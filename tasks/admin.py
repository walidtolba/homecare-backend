from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Demand, Task, Team
from users.models import User
import numpy as np
import pandas as pd
from pyomo.environ import *
import itertools
import osmnx as ox
import networkx as nx

@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    # readonly_fields = ['type', 'title','state','creation_date',  'latitude', 'longitude', 'address','is_urgent', 'creator', 'user']
    actions = ['run_or_system']
    @admin.action(description="Run the Optimization system")
    def run_or_system(self, request, queryset):
        place_point = (36.24608632104293, 6.590354969520524)

        G = ox.graph_from_point(place_point, network_type='drive', simplify=False, retain_all=False)
        G = ox.utils_graph.get_largest_component(G, strongly=True)
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)

        num_patients = queryset.count() + 1
        print(num_patients)
        drivers = list(User.objects.filter(profile__type='Driver', profile__is_absent=False, profile__is_verified=True, team=None))#I modified this
        max_vehicle_count = len(drivers)
        if not max_vehicle_count:
            self.message_user(
            request,
                "There is no driver available",
            messages.WARNING,
            )
            return
        print(max_vehicle_count)
        demands = list(queryset)
        for demand in demands:
            if demand.state in ('F', 'C', 'T'):
                self.message_user(
                request,
                    "There is an unavailable demand",
                messages.WARNING,
                )
                return

        points = { 0:(36.24608632104293, 6.590354969520524)}
        for i in range(len(demands)):
            points[i + 1] = (demands[i].latitude, demands[i].longitude)
        print(points)

        I = set(range(0,num_patients))
        temps_service = [30 if x != 0 else 0 for x in range(num_patients)]


        matrice = np.zeros(num_patients ** 2)
        temps_trajet = matrice.reshape(num_patients,num_patients)

        for i in range(num_patients):
            for j in range(num_patients):
                if i != j :
                    print(i, j)
                    origin_node =ox.distance.nearest_nodes(G, points[i][1],points[i][0])
                    destination_node =ox.distance.nearest_nodes(G, points[j][1],points[j][0])
                    route = nx.shortest_path(G, origin_node, destination_node, weight='travel_time')
                    temps_trajet[i,j] = round(sum(ox.utils_graph.get_route_edge_attributes(G, route, 'travel_time')) / 60)
                    print('time: ' + str(temps_trajet[i,j]))
        

        mat = np.zeros(num_patients ** 2)
        distance = mat.reshape(num_patients,num_patients)

        for i in I:
            for j in I:
                if i!=j:
                    distance[i,j] = temps_trajet[i, j] + temps_service[j]
                    print('distance: ' + str(distance[i, j]))

        

            
        model = ConcreteModel()  

        model.patient = Set(initialize=range(num_patients))
        model.vehicles = Set(initialize=range(max_vehicle_count))
        
        model.x = Var(model.patient,model.patient,model.vehicles, within=Binary)
        
        model.obj_total_cost = Objective(sense=minimize, expr=
                sum(distance[i,j] * model.x[i, j, k]
                    for i in range(num_patients)
                    for j in range(num_patients) if j != i
                    for k in range(max_vehicle_count)
                ))
        
        model.c=ConstraintList()
        
    # Every patient should be visited by just one driver
        for j in range( 1,num_patients):
            model.c.add(sum(model.x[i, j, k] if i != j else 0 for i in range(num_patients) for k in range(max_vehicle_count)) == 1)
      
    # drive in = out = origin
        for k in range(max_vehicle_count):
            model.c.add(sum(model.x[0, j, k] for j in range(1,num_patients)) - sum(model.x[i, 0, k] for i in range(1,num_patients)) == 0)
            model.c.add(sum(model.x[0, j, k] for j in range(1,num_patients)) <= 1)

    # patient_in = patient_out
        for k in range(max_vehicle_count):
            for j in range(num_patients):
                model.c.add(sum(model.x[i, j, k] if i != j else 0 for i in range(num_patients)) - sum(model.x[j, i, k] for i in range(num_patients)) == 0)

    # work_time + driving_time <= 7h
        for k in range(max_vehicle_count):
            model.c.add(sum(distance[i,j]* model.x[i,j,k] if i!=j else 0 for i in range(num_patients) for j in range(num_patients)) <= 420)

    # work_time <= 3h
        for k in range(max_vehicle_count):
            model.c.add(sum(temps_service[j] * model.x[i,j,k] if i!=j else 0  for i in range(num_patients) for j in range(num_patients)) <= 180)

    # sub-tours
        subtours = []
        for i in range(2,num_patients):
            subtours += itertools.combinations(range(1,num_patients), i)

        for s in subtours:
            model.c.add(sum(model.x[i, j, k] if i !=j else 0 for i, j in itertools.permutations(s,2) for k in range(max_vehicle_count)) <= len(s) - 1)

    ##SolverFactory('glpk', executable='C:\\Users\\USER\\Downloads\\winglpk-4.65\\glpk-4.65\\w64\\glpsol').solve(model, tee=False)
        results = SolverFactory('glpk', executable='/usr/bin/glpsol').solve(model, tee=False)
        if not (results.solver.status == SolverStatus.ok):
            self.message_user(
                request,
                    "System failed to create tasks.",
                messages.WARNING,
                )
            return
        if  results.solver.termination_condition == TerminationCondition.infeasible:
            self.message_user(
                request,
                    "Can't find an optimal solution.",
                messages.WARNING,
                )
            return
        List=list(model.x.keys())

        for k in range(max_vehicle_count):
            if 1 == sum(model.x[0, j, k]() for j in range(1, num_patients)):
                counter = 0
                team = Team(driver=drivers[k])
                team.save()
                print("Driver ",k+1,":")
                j = 0
                print(points[j], end=' ')
                while True:
                    for i in List:
                        if model.x[i]()==1 and k == i[2] and j == i[0]:
                            j = i[1]
                            if i[1] != 0:
                                task = Task(order=counter, team=team, demand=demands[j-1])
                                demand[j-1].state = 'T'
                                task.save()
                                demand[j-1].save()
                                counter += 1
                            print('->', points[j], end=' ')
                            break
                    if j == 0:
                        break
                    
            print(model.obj_total_cost())
            self.message_user(
            request,
            ngettext(
                "%d task has been created successfully.",
                "%d tasks has been created successfuly.",
                len(demands),
            )
            % len(demands)
            ,
            messages.SUCCESS,
        )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['order', 'state', 'creation_date', 'demand', 'user', 'team']
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ['turn', 'driver']
  

