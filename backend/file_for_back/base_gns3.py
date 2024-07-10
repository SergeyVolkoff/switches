
from gns3fy import Gns3Connector, Project, Node, Link
from tabulate import tabulate

from rich import print
from rich.theme import Theme
from rich.console import Console
my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
)
console = Console(theme=my_colors)

class Base_gns():

    def __init__(self,name_lab):

        """ Определение коннектора(connector) и проекта (lab) """

        self.server_url = "http://10.27.193.245:3080"
        self.connector = Gns3Connector(url=self.server_url)
        self.list_labs = (tabulate(self.connector.projects_summary(is_print=False), headers=["Project Name"]))
        print(self.list_labs)
        self.name_lab = name_lab
        # self.name_lab = input("Input lab name: ")
        

    def all_proj (self):

        """ Возвращает перечень всех лаб в ГНС"""

        return tabulate(
            self.connector.projects_summary(is_print=False),
            headers=["Project Name", "Project ID", "Total Nodes", "Total Links", "Status"],
        )

    def get_ver_gns(self):

        """ Вернет версию GNS - абсолютно бесполезная хрень, если выкл обновление """

        gns_ver = self.connector.get_version()
        return f"GNS3 ver is {gns_ver}"
        
    def get_lab_status(self):

        """ Вернет lab_id, статус моей лабы """

        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        #lab.close()
        print(lab.project_id)
        return f"GNS3 lab_name: {lab.name}, lab_id:{lab.project_id}, lab status: {lab.status}"
    
    def get_nodes(self):

        """ Вернет все узлы в лабе"""

        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
        lab.start_nodes(poll_wait_time=5)
        console.print(f"*** ALL nodes in {lab.name} lab ***",style='success')
        return  lab.nodes_summary()
    
    def start_node(self):

        """ Запуск 2go узла в проекте"""
        
        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
        r2 = Node(
            project_id=lab.project_id, 
            name='R2',
            connector=self.connector
            ) # создаем экз-р устр-ва
        
        r2.get()
        r2.start()
        console.print (f'Node {r2.name} {r2.status}',style='success')


    def stop_node(self):
        """ Запуск 2go узла в проекте"""
        
        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
         # links_summary = lab.links_summary(is_print=False)
        # print(
        #     tabulate(links_summary,headers=["Node R1","port R1","Node R2","port R2"])
        # )
        r2 = Node(
            project_id=lab.project_id, 
            name='R2',
            connector=self.connector
            ) # создаем экз-р устр-ва
        r2.get()
        r2.stop()
        console.print (f'Node {r2.name} {r2.status}',style='success')
        # link_r2_DUT = r2.links[1]
        # print(link_r2_DUT)
        # link_r2_DUT.get()
        # link_r2_DUT.delete()

    def start_nodes_from_project(self):

        lab = Project(name=self.name_lab , connector=self.connector )
        lab.get()
        lab.open() # open lab
        lab.start_nodes(poll_wait_time=5)
        console.print(f"*** ALL nodes in {lab.name} lab ***",style='success')
        return  lab.nodes_summary()


if __name__=="__main__":
    gns= Base_gns()
    # print (gns.get_ver_gns(),'\n')
    # print(gns.all_proj(),'\n')
    print(gns.get_lab_status(),'\n')
    
    # print(gns.start_node())
    # print(gns.start_nodes_from_project())
    # print( gns.get_nodes(),'\n')