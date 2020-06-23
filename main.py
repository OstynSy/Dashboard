import sys
import time
import weather
import PIL
import compstats
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QInputDialog, QFrame, QWidget, QBoxLayout, QGridLayout, \
    QHBoxLayout, QProgressBar

# start: 6/8/2020


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Dashboard'
        self.x = 0
        self.y = 0
        self.width = 2000
        self.height = 1500
        self.background_color = 'background-color: #3C3F41'
        #self.icon = QtGui.QIcon('.png')
        self.init_ui()

    def init_ui(self):

        # main Window
        self.setWindowTitle(self.title)
        #self.setWindowIcon(self.icon)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet(self.background_color)

        # Dashboard header
        dash_label = QLabel(self)
        dash_label.setText('   Dashboard')
        dash_label.setFont(QFont('Montserrat', 30, QFont.Bold))
        dash_label.setGeometry(0, 0, self.width, 100)
        dash_label.setStyleSheet('background-color: #1E2127 ; color:white')

        # Date
        self.date_label = QLabel(self)
        self.date_label.setFont(QFont('Montserrat', 20, QFont.Bold))
        self.date_label.setGeometry(1600, 15, 340, 70)
        self.date_label.setStyleSheet('background:transparent; color:white')

        # Time
        self.time_label = QLabel(self)
        self.time_label.setFont(QFont('Montserrat', 20, QFont.Bold))
        self.time_label.setGeometry(1630, 50, 250, 30)
        self.time_label.setStyleSheet('background:transparent; color:white')

        # Time & Date Refresher
        date_timer = QTimer(self)
        date_timer.timeout.connect(self.display_time)
        date_timer.start(1000)
        self.display_time()
        self.display_date()

        # Display Weather
        weather_label = QLabel(self)
        weather_label.setText(' Weather Forecast        Location: Lafayette, CA, US')
        weather_label.setFont(QFont('Montserrat', 13, QFont.Bold))
        weather_label.setGeometry(10, 120, 1800, 40)
        weather_label.setStyleSheet('background-color: #1E2127 ; color:white')

        weather_background_label = QLabel(self)
        weather_background_label.setGeometry(10, 155, 1800, 150)
        weather_background_label.setStyleSheet('background-color: #19445E ; border: 3px solid #1E2127')

        # Weather timer
        weather_timer = QTimer(self)
        weather_timer.timeout.connect(self.display_weather)
        weather_timer.start(3600000)
        self.display_weather()

        # Display Gpu header
        gpu_label = QLabel(self)
        gpu_label.setText(' Computer Stats           Recommended Temp: 70-85 °C')
        gpu_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        gpu_label.setGeometry(10, 317, 650, 40)
        gpu_label.setStyleSheet('background:#1E2127; color:white')

        gpu_background_label = QLabel(self)
        gpu_background_label.setGeometry(10, 350, 650, 130)
        gpu_background_label.setStyleSheet('background-color: #19445E ; border: 3px solid #1E2127')

        # GPU Data
        self.gpu_info_label = QLabel(self)
        self.gpu_info_label.setFont(QFont('Montserrat', 13, QFont.Bold))
        self.gpu_info_label.setGeometry(85, 385, 500, 60)
        self.gpu_info_label.setStyleSheet('background:transparent; color:white')

        # CPU Data
        self.cpu_info_label = QLabel(self)
        self.cpu_info_label.setFont(QFont('Montserrat', 13, QFont.Bold))
        self.cpu_info_label.setGeometry(410, 375, 500, 60)
        self.cpu_info_label.setStyleSheet('background:transparent; color:white')

        # RAM Data
        self.ram_info_label = QLabel(self)
        self.ram_info_label.setFont(QFont('Montserrat', 13, QFont.Bold))
        self.ram_info_label.setGeometry(410, 410, 90, 60)
        self.ram_info_label.setStyleSheet('background:transparent; color:white')

        # Display harddrive header
        harddrive_label = QLabel(self)
        harddrive_label.setText(' Current Hard Drive Capacity')
        harddrive_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        harddrive_label.setGeometry(10, 490, 650, 40)
        harddrive_label.setStyleSheet('background:#1E2127; color:white')

        harddrive_background_label = QLabel(self)
        harddrive_background_label.setGeometry(10, 530, 650, 130)
        harddrive_background_label.setStyleSheet('background-color: #19445E ; border: 3px solid #1E2127')

        # C: Label
        c_drive_label = QLabel(self)
        c_drive_label.setText('C:')
        c_drive_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        c_drive_label.setGeometry(15, 551, 300, 30)
        c_drive_label.setStyleSheet('background-color: transparent; color:white')

        # G: Label
        g_drive_label = QLabel(self)
        g_drive_label.setText('G:')
        g_drive_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        g_drive_label.setGeometry(15, 595, 300, 30)
        g_drive_label.setStyleSheet('background-color: transparent; color:white')

        # compstats refresher
        gpu_timer = QTimer(self)
        gpu_timer.timeout.connect(self.display_compstat)
        gpu_timer.start(500)
        self.display_compstat()

        harddrive_timer = QTimer(self)
        harddrive_timer.timeout.connect(self.display_harddrive)
        harddrive_timer.start(1000)
        self.display_harddrive()
        compstats.get_cpu_ram_stats()

    def display_compstat(self):
        # GPU usuage
        gpu_data = compstats.get_gpu_stats()

        gpu_label = QLabel(self)
        gpu_label.setText('GPU: ' + gpu_data[0][0])
        gpu_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        gpu_label.setGeometry(15, 350, 500, 40)
        gpu_label.setStyleSheet('background:transparent; color:white')
        self.gpu_info_label.setText('Load: ' + str(round(gpu_data[0][1], 2)) + '%\nTemp: ' + str(gpu_data[0][2]))

        # CPU Usage
        cpu_ram_data = compstats.get_cpu_ram_stats()

        cpu_label = QLabel(self)
        cpu_label.setText('CPU: ')
        cpu_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        cpu_label.setGeometry(340, 385, 70, 40)
        cpu_label.setStyleSheet('background:transparent; color:white')
        self.cpu_info_label.setText(str(cpu_ram_data[0]) + '%')

        # RAM Usage
        ram_label = QLabel(self)
        ram_label.setText('RAM: ')
        ram_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        ram_label.setGeometry(340, 420, 70, 40)
        ram_label.setStyleSheet('background:transparent; color:white')
        self.ram_info_label.setText(str(cpu_ram_data[1]) + '%')

    def display_harddrive(self):

        def get_progress_color(value):
            progress_color = ''
            if value <= 25:
                # green
                progress_color = 'QProgressBar::chunk{background-color: #2FB940;}'
            elif value > 25 and value <=50:
                # blue
                progress_color = 'QProgressBar::chunk{background-color: #26A0DA;}'
            elif value > 50 and value <=75:
                # orange
                progress_color = 'QProgressBar::chunk{background-color: #F99D31;}'
            else:
                # red
                progress_color = 'QProgressBar::chunk{background-color: #DA2626;}'

            return progress_color

        harddrive_data = compstats.get_disk_stats()

        # C: progress bar
        c_percent_used = (harddrive_data[0][1] / harddrive_data[0][0]) * 100
        self.c_progress = QProgressBar(self)
        self.c_progress.setValue(c_percent_used)
        self.c_progress.setFont(QFont('Montserrat', 15, QFont.Bold))
        self.c_progress.setGeometry(50, 557, 120, 20)
        self.c_progress.setTextVisible(False)
        self.c_progress.setStyleSheet(get_progress_color(c_percent_used))

        # G: progress bar
        g_percent_used = (harddrive_data[1][1] / harddrive_data[1][0]) * 100
        self.g_progress = QProgressBar(self)
        self.g_progress.setValue(g_percent_used)
        self.g_progress.setFont(QFont('Montserrat', 15, QFont.Bold))
        self.g_progress.setGeometry(50, 600, 120, 20)
        self.g_progress.setTextVisible(False)
        self.g_progress.setStyleSheet(get_progress_color(g_percent_used))

        # C: display GB
        c_label = QLabel(self)
        c_label.setText(' ' + str(round(c_percent_used, 2)) + '%    ' + str(harddrive_data[0][1]) + ' GB / ' + str(harddrive_data[0][0]) + ' GB      ' + str(harddrive_data[0][2]) + ' GB Free')
        c_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        c_label.setGeometry(170, 557, 500, 20)
        c_label.setStyleSheet('background:transparent; color:white')

        # G: display GB
        g_label = QLabel(self)
        g_label.setText(' ' + str(round(g_percent_used, 2)) + '%    ' + str(harddrive_data[1][1]) + ' GB / ' + str(harddrive_data[1][0]) + ' GB      ' + str(harddrive_data[1][2]) + ' GB Free')
        g_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        g_label.setGeometry(170, 600, 500, 20)
        g_label.setStyleSheet('background:transparent; color:white')

    def display_weather(self):
        weather_data = weather.get_weather()

        #weather data
        day_x_position = 45
        day_y_position = 160
        day_width_scale = 120
        day_height_scale = 30

        temp_x_position = 60
        temp_y_position = 270
        temp_width_scale = 100
        temp_height_scale = 30

        maxmin_x_position = 155
        maxmin_y_position = 145
        maxmin_width_scale = 1200
        maxmin_height_scale = 150

        image_x_position = 50
        image_y_position = 180
        image_width_scale = 100
        image_height_scale = 100
        spacing = 220
        weather_transparent_style ='background-color: transparent ; color:white'

        # day
        day_label = QLabel(self)
        day_label.setText('Today')
        day_label.setFont(QFont('Montserrat', 15, QFont.Bold))
        day_label.setGeometry(day_x_position, day_y_position, day_width_scale, day_height_scale)
        day_label.setStyleSheet(weather_transparent_style)

        for count in range(1, 8):
            day_x_position += spacing
            day1_label = QLabel(self)
            day1_label.setText(weather_data[count][0])
            day1_label.setFont(QFont('Montserrat', 15, QFont.Bold))
            day1_label.setGeometry(day_x_position, day_y_position, day_width_scale, day_height_scale)
            day1_label.setStyleSheet(weather_transparent_style)

        # current temp
        for count in range(0, 8):
            temp_label = QLabel(self)
            temp_label.setText(str(weather_data[count][1]) + ' °F')
            temp_label.setFont(QFont('Montserrat', 15, QFont.Bold))
            temp_label.setGeometry(temp_x_position, temp_y_position, temp_width_scale, temp_height_scale)
            temp_label.setStyleSheet(weather_transparent_style)
            temp_x_position += spacing

        # max and min temp
            forecast_label = QLabel(self)
            forecast_label.setText('H: ' + str(weather_data[count][2]) + ' °F' + '\nL: ' + str(weather_data[count][3]) + ' °F')
            forecast_label.setFont(QFont('Montserrat', 10, QFont.Bold))
            forecast_label.setGeometry(maxmin_x_position, maxmin_y_position, maxmin_width_scale, maxmin_height_scale)
            forecast_label.setStyleSheet(weather_transparent_style)
            maxmin_x_position += spacing

        # weather images
            weather_image_label = QLabel(self)
            weather_image = QPixmap('C:\\Users\\ostyn\\PycharmProjects\\dashboard\\weatherimages\\' + weather_data[count][4] + '.png')
            scaled_weather_image = weather_image.scaled(80, 80)
            weather_image_label.setPixmap(scaled_weather_image)
            weather_image_label.setGeometry(image_x_position, image_y_position, image_width_scale, image_height_scale)
            weather_image_label.setStyleSheet(weather_transparent_style)
            image_x_position += spacing

    def display_date(self):
        current_date = time.strftime('%A, %d %B %Y\n')
        self.date_label.setText(current_date)

    def display_time(self):
        current_time = time.strftime('%I : %M : %S %p')
        self.time_label.setText(current_time)

        if time.strftime('%I') == '12' and time.strftime('%p') == 'AM':
            self.display_date()

    def display(self):
        self.showMaximized()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    program = Window()
    program.display()
    sys.exit(App.exec_())
