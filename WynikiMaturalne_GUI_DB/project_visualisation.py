from typing import List
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QStackedWidget, QCheckBox, QMessageBox
import pyqtgraph as pg
import json


class MaturaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wyniki Maturalne')
        self.setGeometry(100, 100, 1200, 800)
        
        self.subject_index = 0
        self.men_chosen = False
        self.women_chosen = False
        self.general_chosen = False
        self.extended_chosen = False
        self.basic_chosen = False
        self.formula2015_chosen = False
        self.formula2023_chosen = False
        
        # Load credentials 
        with open('.venv/credentials.json') as config_file:
            config = json.load(config_file)
        # get the credentials
        db_user = config['DB_USER']
        db_password = config['DB_PASSWORD']
        db_host = config['DB_HOST']
        db_port = config['DB_PORT']
        db_name = config['DB_NAME']
        # Set up the database connection
        try:
            self.engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
        except:
            self.show_error("Nie można nawiązać połączenia z serwerem!")
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Plot graph
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setBackground("w")
        
        # Navigation panel
        self.navigation_panel = QListWidget()
        self.navigation_panel.addItems(["Język polski", "Język angielski", "Język niemiecki",
                                        "Matematyka", "Geografia", "Fizyka", "Historia"])
        self.navigation_panel.currentItemChanged.connect(self.update_index)
        self.navigation_panel.setFixedWidth(250)
        main_layout.addWidget(self.navigation_panel)
        
        # Central display area
        self.central_display = QStackedWidget()
        
        # Add the dashboard view
        self.dashboard_view = self.create_dashboard_view()
        self.central_display.addWidget(self.dashboard_view)
        main_layout.addWidget(self.central_display)
        
        # Set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        self.results_men = []
        self.results_women = []
        self.results_general =  []
        self.years = []
        
        self.subject_map = {
                    0: "język polski",
                    1: "język angielski",
                    2: "język niemiecki",
                    3: "matematyka",
                    4: "geografia",
                    5: "fizyka",
                    6: "historia"
                }
            
    def create_dashboard_view(self):
        # Create a dashboard view
        view = QWidget()
        layout = QVBoxLayout()

        # run button
        self.run_button = QPushButton()
        self.run_button.setText("Wykonaj")
        self.run_button.clicked.connect(self.run_button_clicked)

        # checkboxes
        self.cbox_kobiety = QCheckBox("Kobiety")
        self.cbox_mezczyzni = QCheckBox("Mężczyźni")
        self.cbox_ogolem = QCheckBox("Ogółem")
        self.cbox_formula2015 = QCheckBox("Formuła 2015")
        self.cbox_formula2023 = QCheckBox("Formuła 2023")
        self.cbox_basic = QCheckBox("Podstawowa")
        self.cbox_extended = QCheckBox("Rozszerzona")

        self.cbox_kobiety.toggled.connect(self.onClickedWomen)
        self.cbox_mezczyzni.toggled.connect(self.onClickedMen)
        self.cbox_ogolem.toggled.connect(self.onClickedGeneral)
        self.cbox_basic.toggled.connect(self.onClickedBasic)
        self.cbox_extended.toggled.connect(self.onClickedExtended)
        self.cbox_formula2015.toggled.connect(self.onClickedFormula2015)
        self.cbox_formula2023.toggled.connect(self.onClickedFormula2023)

        layout.addWidget(self.cbox_kobiety)
        layout.addWidget(self.cbox_mezczyzni)
        layout.addWidget(self.cbox_ogolem)
        layout.addWidget(self.cbox_basic)
        layout.addWidget(self.cbox_extended)
        layout.addWidget(self.cbox_formula2015)
        layout.addWidget(self.cbox_formula2023)

        layout.addWidget(self.run_button)

        # plot
        layout.addWidget(self.plot_graph)
        self.plot_graph.setFixedSize(800, 600)

        view.setLayout(layout)
        return view
    
    def plot_results(self, name: str, x_arr: List[int], y_arr: List[float], pen, brush: str):
        self.plot_graph.addLegend(offset=(-5, 10))
        self.plot_graph.setLabel("bottom", "Rok")
        self.plot_graph.setLabel("left", "Wyniki")
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.plot(
            x_arr,
            y_arr,
            name=name,
            pen=pen,
            symbol="o",
            symbolBrush=brush
        )
    
    def onClickedWomen(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.women_chosen = True
        else:
            self.women_chosen = False
        
    def onClickedMen(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.men_chosen = True
        else:
            self.men_chosen = False

    def onClickedGeneral(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.general_chosen = True
        else:
            self.general_chosen = False
    
    def onClickedExtended(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.extended_chosen = True
        else:
            self.extended_chosen = False
    
    def onClickedBasic(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.basic_chosen = True
        else:
            self.basic_chosen = False    
    
    def onClickedFormula2015(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.formula2015_chosen = True
        else:
            self.formula2015_chosen = False  
    
    def onClickedFormula2023(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.formula2023_chosen = True
        else:
            self.formula2023_chosen = False   
    
    '''
        Update chosen subject index
    '''
    def update_index(self, current, previous):
        print(self.navigation_panel.row(previous))
        if current:
            self.subject_index = self.navigation_panel.row(current)
        self.plot_graph.clear()
        
    def update_plot(self):
        self.plot_graph.clear()
        if self.men_chosen:
            self.plot_men()
        if self.women_chosen:
            self.plot_women()
        if self.general_chosen:
            self.plot_general()
        
    '''
        Handle getting data and plotting results with specified settings - show error if settings are incorrect
    '''
    def run_button_clicked(self):
        error = False
        if ( self.basic_chosen or self.extended_chosen ) and ( self.women_chosen or self.men_chosen or self.general_chosen ) \
            and ( self.formula2015_chosen or self.formula2023_chosen ):
            if ( self.basic_chosen and self.extended_chosen ) or ( self.formula2015_chosen and self.formula2023_chosen ):
                error = True
            else:
                subject = self.subject_map[self.subject_index]
                if self.basic_chosen:
                    level = "podstawowy"
                else:
                    level = "rozszerzony"
                
                if self.formula2015_chosen:
                    formula = "formuła 2015"
                else:
                    formula = "formuła 2023"
                
                if self.men_chosen:
                    self.results_men = self.get_data("mężczyźni", subject, level, formula)
                if self.women_chosen:
                    self.results_women = self.get_data("kobiety", subject, level, formula)
                if self.general_chosen:
                    self.results_general = self.get_data("ogółem", subject, level, formula)
                self.update_plot()
        else:
            error = True
        
        if error:
            self.show_error("Wybierz dobre parametry")
            
    '''
        Create and send SQL query to det specified data
    '''
    def get_data(self, group: str, subject: str, level: str, formula: str):
        self.years = self.session.execute(text(f"SELECT DISTINCT rok FROM Egzamin_Maturalny em \
                                                JOIN Formula f ON em.formula_id = f.formula_id \
                                                WHERE f.formula = '{formula}'")).fetchall()
        self.years = self.make_1Darray_from_tuples(self.years)
        return self.make_1Darray_from_tuples(self.session.execute(text(f"SELECT em.wynik \
                                                                        FROM Egzamin_Maturalny em \
                                                                        JOIN Plec p ON em.plec_id = p.plec_id \
                                                                        JOIN Przedmioty pr ON em.przedmiot_id = pr.przedmiot_id \
                                                                        JOIN Formula fr ON em.formula_id = fr.formula_id \
                                                                        LEFT JOIN Poziom po ON em.poziom_id = po.poziom_id \
                                                                        WHERE p.plec = '{group}'  \
                                                                        AND pr.przedmiot = '{subject}' \
                                                                        AND po.poziom = '{level}' \
                                                                        AND fr.formula = '{formula}'")).fetchall())


    '''
        Plot women data if available
    '''
    def plot_women(self):
        try:
            pen = pg.mkPen(color=(255, 0, 0))
            self.plot_results("Kobiety", self.years, self.results_women, pen=pen, brush="r")
        except:
            self.show_error("Błąd danych!")
        
    '''
        Plot men data if available
    '''
    def plot_men(self):
        try:
            pen = pg.mkPen(color=(0, 0, 255))
            self.plot_results("Meżczyźni", self.years, self.results_men, pen=pen, brush="b")
        except:
            self.show_error("Błąd danych!")
        
    '''
        Plot general data if available
    '''
    def plot_general(self):
        try:
            pen = pg.mkPen(color=(0, 0, 0))
            self.plot_results("Ogółem", self.years, self.results_general, pen=pen, brush="k")
        except:
            self.show_error("Błąd danych!")
    
    '''
        Convert data received from db to numpy array
    '''
    def make_1Darray_from_tuples(self, data: List):
        result = []
        for elem in data:
            result.append(elem[0])
        result = np.array(result)
        return result
        
    def show_error(self, msg_info: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(msg_info)
        msg.setWindowTitle("Error")
        msg.exec_()
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MaturaApp()
    mainWin.show()
    sys.exit(app.exec_())
    
