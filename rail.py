import ev3dev.ev3 as ev3
from time import sleep
ma = ev3.LargeMotor('outA')
mb = ev3.LargeMotor('outB')
mc = ev3.LargeMotor('outC')
md = ev3.LargeMotor('outD')

SPEED = 300
TIME = 850

# bucket 1:
# TIME = 850
# BUCKET 2:
# TIME = 2100, BUT NEEDS TO TURN COUTER CLOCKWISE A BIT TO BE AT CENTER

ma.run_timed(speed_sp=-SPEED, time_sp=TIME)
mb.run_timed(speed_sp=SPEED, time_sp=TIME)
mc.run_timed(speed_sp=SPEED, time_sp=TIME)
md.run_timed(speed_sp=-SPEED, time_sp=TIME)

sleep(2)

ma.run_timed(speed_sp=SPEED, time_sp=TIME+200)
mb.run_timed(speed_sp=-SPEED, time_sp=TIME+200)
mc.run_timed(speed_sp=-SPEED, time_sp=TIME+200)
md.run_timed(speed_sp=SPEED, time_sp=TIME+200)
