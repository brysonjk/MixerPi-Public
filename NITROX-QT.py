#!.venv/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, \
      QHBoxLayout, QLabel, QSplashScreen,QPushButton, QSpacerItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import O2SENSOR_old as o2
import threading


#pid = o2.PID(Kp=1.0, Ki=5.0, Kd=0.1, setpoint=o2.targetOxygen)
#pid.output_limits = (o2.PID_MIN, o2.PID_MAX)  # Limit PID output to a range

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.ema0 = o2.EMA(k=4)
        self.setpoint = o2.targetOxygen
        self.pid = o2.initializePID(1.0, 5.0, 0.1, o2.targetOxygen)
        # o2.start_PID_Thread(self.pid, self.ema0, o2.calValue0)
        self.start_ema_thread()
        # self.start_pid_thread()
        self.initUI()
        self.start_timers()

    def start_ema_thread(self):
        """Start the EMA thread."""
        ema_thread = threading.Thread(target=o2.ema_thread, args=(self.ema0, o2.get_chan0_data, 0.01))
        ema_thread.daemon = True
        ema_thread.start()

    # def start_pid_thread(self):
    #     """Start the PID thread."""
    #     def pid_task():
    #         while True:
    #             if o2.calibrated0:
    #                 ema_value = self.ema0.getEmaValue()
    #                 oxygen_reading = (ema_value / o2.calValue0) * 20.9
    #                 pid_output = self.pid(oxygen_reading)

    #                 # Update the PID label in the GUI
    #                 self.pid_label.setText(f"{pid_output:.2f}")
    #     pid_thread = threading.Thread(target=pid_task)
    #     pid_thread.daemon = True
    #     pid_thread.start()

    def initUI(self):
        """Initialize the GUI."""
        self.setWindowTitle('Dark Water Diving --- Nitrox Mixer')
        self.setGeometry(100, 100, 800, 450)

        grid = QGridLayout()

        # Titles
        grid.addWidget(self.create_label('Dark Water Diving', 32), 0, 0, 1, 3, alignment=Qt.AlignCenter)
        grid.addWidget(self.create_label('Nitrox Mixer', 24), 1, 0, 1, 3, alignment=Qt.AlignCenter)

        # # Setpoint controls
        # grid.addWidget(self.create_label("Setpoint =", 32), 2, 0, alignment=Qt.AlignRight | Qt.AlignVCenter)
        # self.setpoint_label = self.create_label(f"{o2.targetOxygen:.1f}", 32)
        # grid.addWidget(self.setpoint_label, 2, 0, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        # # + and - buttons in a vertical layout
        # #vbox_buttons = QVBoxLayout()
        # hbox_Setpoint = QHBoxLayout()
        # self.increase_button = QPushButton("+", self)
        # self.increase_button.setStyleSheet("font-size: 24px; font-weight: bold;")
        # self.increase_button.clicked.connect(self.increase_setpoint)
        # hbox_Setpoint.addWidget(self.increase_button)

        # self.decrease_button = QPushButton("-", self)
        # self.decrease_button.setStyleSheet("font-size: 24px; font-weight: bold;")
        # self.decrease_button.clicked.connect(self.decrease_setpoint)
        # hbox_Setpoint.addWidget(self.decrease_button)

        
        # # Place the hbox in the grid
        # hbox_widget = QWidget()
        # hbox_widget.setLayout(hbox_Setpoint)
        # grid.addWidget(hbox_widget, 2, 1, alignment=Qt.AlignRight)
        # #grid.addWidget(hbox_widget, 2, 2, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        # PID label
        #hbox_pid = QHBoxLayout()
        #hbox_pid.addWidget(self.create_label("PID =", 32))
        #grid.addWidget(self.create_label("PID =", 32), 2, 1, alignment=Qt.AlignRight | Qt.AlignVCenter)
        #self.pid_label = self.create_label(f"000", 32)
        #hbox_pid.addWidget(self.pid_label)#, 2, 2, 1, 1, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        #hbox_widget = QWidget()
        #hbox_widget.setLayout(hbox_pid)
        #grid.addWidget(hbox_widget, 2, 2, alignment=Qt.AlignLeft)


        # Oxygen reading and MOD
        self.reading_label = self.create_label('12.34% O²', 128)
        grid.addWidget(self.reading_label, 4, 0, 1, 3, alignment=Qt.AlignCenter)
        self.mod_label = self.create_label('MOD = 123', 32)
        grid.addWidget(self.mod_label, 5, 0, 1, 3, alignment=Qt.AlignCenter)

        # Calibrate button
        self.calibrate_button = QPushButton("Re-Calibrate", self)
        self.calibrate_button.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.calibrate_button.clicked.connect(self.on_calibrate_button_clicked)
        grid.addWidget(self.calibrate_button, 6, 0, 1, 3, alignment=Qt.AlignCenter)

        self.setLayout(grid)

    def create_label(self, text, font_size):
        """Create a QLabel with specified text and font size."""
        label = QLabel(text, self)
        label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        return label
    
    def increase_setpoint(self):
        """Increase the setpoint value."""
        o2.targetOxygen += 0.5
        self.pid.setpoint = o2.targetOxygen
        self.setpoint_label.setText(f"{o2.targetOxygen:.1f}")

    def decrease_setpoint(self):
        """Decrease the setpoint value."""
        o2.targetOxygen -= 0.5
        self.pid.setpoint = o2.targetOxygen
        self.setpoint_label.setText(f"{o2.targetOxygen:.1f}")

    def start_timers(self):
        """Start timers for updating readings and MOD."""
        self.start_timer(self.update_reading, 500)
        self.start_timer(self.update_mod, 500)

    def start_timer(self, callback, interval):
        """Start a QTimer with a callback and interval."""
        timer = QTimer(self)
        timer.timeout.connect(callback)
        timer.start(interval)

    def update_reading(self):
        """Update the oxygen reading."""
        reading = self.ema0.getEmaValue()
        O2_S0 = ((reading / o2.calValue0) * 20.9) if o2.calibrated0 else 0
        print(f"Oxygen Reading: {O2_S0:.1f}%")
        self.reading_label.setText(f"{O2_S0:.1f}% o2")
        #self.o2SensorMV_label.setText(f"{reading*o2.MULTIPLIER:.2f}")

    def update_mod(self):
        """Update the MOD value."""
        if o2.calibrated0:
            MOD_S0 = ((1.4 / ((self.ema0.getEmaValue() / o2.calValue0) * 20.9 * 0.01)) - 1) * 33
            self.mod_label.setText(f"MOD = {MOD_S0:.0f}")
        else:
            self.reading_label.setText("0.00% O²")

    def update_setpoint(self):
        """Update the setpoint value."""
        #O2_SP0 = ((self.e))

    def on_calibrate_button_clicked(self):
        """Handle the Calibrate button click."""
        self.calibrate_button.setEnabled(False)  # Disable the button during calibration
        o2.calibrated0 = 0 
        run_calibration(self.ema0, self.on_calibration_complete)

    def on_calibration_complete(self):
        """Re-enable the Calibrate button after calibration."""
        self.calibrate_button.setEnabled(True)



def run_calibration(ema_instance, callback):
    """Run the calibration process in a separate thread."""
    def calibration_task():
        if not o2.calibrated0:
            print('Calibrating Channel 0...')
            o2.calValue0 = o2.calibrate(ema_instance)
            o2.calibrated0 = o2.calValue0 != 0
            print('Calibration complete.' if o2.calibrated0 else 'Calibration failed.')
        callback()

    threading.Thread(target=calibration_task).start()


def main():
    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap(800, 450)
    splash_pix.fill(Qt.black)  # Fill the pixmap with a black background
    splash = QSplashScreen(splash_pix)
    splash.showMessage("Loading\n Dark Water Diving --- Nitrox Mixer...\nCalibrating sensors...", Qt.AlignCenter | Qt.AlignBottom, Qt.white)
    splash.show()

    # Process events to ensure the splash screen is displayed immediately
    app.processEvents()

    # Create the main application window
    ex = App()

    # Define a callback to close the splash screen and show the main window
    def on_calibration_complete():
        splash.close()
        ex.show()

    # Run the calibration process and pass the callback
    run_calibration(ex.ema0, on_calibration_complete)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()