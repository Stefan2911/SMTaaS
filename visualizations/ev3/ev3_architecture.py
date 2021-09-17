from urllib.request import urlretrieve

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.custom import Custom

with Diagram("EV3 System Architecture", show=False, filename="ev3_architecture", direction="LR"):
    with Cluster("EV3"):
        with Cluster("Monitoring"):
            monitoring_url = "https://cdn-icons-png.flaticon.com/512/857/857779.png"
            monitoring_icon = "monitoring.png"
            urlretrieve(monitoring_url, monitoring_icon)

            monitoring = Custom("Monitoring", monitoring_icon)

            with Cluster("Monitoring Components"):
                monitoring_battery_url = "https://cdn-icons-png.flaticon.com/512/3103/3103277.png"
                monitoring_battery_icon = "monitoring_battery.png"
                urlretrieve(monitoring_battery_url, monitoring_battery_icon)

                monitoring_battery = Custom("Battery", monitoring_battery_icon)

                monitoring_connectivity_url = "https://cdn-icons-png.flaticon.com/512/1057/1057254.png"
                monitoring_connectivity_icon = "monitoring_connectivity.png"
                urlretrieve(monitoring_connectivity_url, monitoring_connectivity_icon)

                monitoring_connectivity = Custom("Connectivity", monitoring_connectivity_icon)

                monitoring_system_utilization_url = "https://cdn-icons-png.flaticon.com/512/689/689379.png"
                monitoring_system_utilization_icon = "monitoring_system_utilization.png"
                urlretrieve(monitoring_system_utilization_url, monitoring_system_utilization_icon)

                monitoring_system_utilization = Custom("System Utilization", monitoring_system_utilization_icon)

        decision_making_url = "https://cdn-icons-png.flaticon.com/512/2752/2752523.png"
        decision_making_icon = "decision_making.png"
        urlretrieve(decision_making_url, decision_making_icon)

        decision_making = Custom("Simplified Decision Module", decision_making_icon)

        cvc4_url = "https://avatars.githubusercontent.com/u/2973223?s=200&v=4"
        cvc4_icon = "cvc4.png"
        urlretrieve(cvc4_url, cvc4_icon)

        cvc4 = Custom("CVC4 Solver", cvc4_icon)

    edge_node = EC2("Edge Node")

    decision_making << Edge() >> monitoring
    monitoring << Edge() >> [monitoring_battery, monitoring_connectivity, monitoring_system_utilization]
    cvc4 << Edge() >> decision_making
    edge_node << Edge() >> decision_making
