import lejos.nxt.Button;
import lejos.nxt.SensorPort;
import lejos.nxt.Sound;
import lejos.nxt.comm.RConsole;
import lejos.util.Delay;


public class main {

	public static void main(String[] args) {
		//RConsole.openUSB(0);
		Sound.beep();
		Delay.msDelay(1000);
		RConsole.println("OK1");
		LEDStrip led = new LEDStrip(SensorPort.S1);
		RConsole.println("OK2");
		while (true){
			led.fadeToRGB(LEDStrip.COLOR_WHITE);
			Delay.msDelay(2000);
			led.fadeToRGB(LEDStrip.COLOR_CYAN);
			Delay.msDelay(2000);
			led.fadeToRGB(LEDStrip.COLOR_MAGENTA);
			Delay.msDelay(2000);
			led.fadeToRGB(LEDStrip.COLOR_YELLOW);
			Delay.msDelay(2000);
			led.fadeToRGB(LEDStrip.COLOR_RED);
			Delay.msDelay(2000);
			led.fadeToRGB(LEDStrip.COLOR_GREEN);
			Delay.msDelay(2000);
			led.fadeToRGB(LEDStrip.COLOR_BLUE);
			Delay.msDelay(2000);
		
		}

	}

}
