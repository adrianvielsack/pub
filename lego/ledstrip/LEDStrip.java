import lejos.nxt.I2CPort;
import lejos.nxt.SensorPort;

public class LEDStrip {

	private SensorPort i2cPort;
	
	public static int COLOR_OFF = 0x000000;
	public static int COLOR_RED = 0xFF0000;
	public static int COLOR_BLUE = 0x0000FF;
	public static int COLOR_GREEN = 0x00FF00;
	public static int COLOR_MAGENTA = 0xFF00FF;
	public static int COLOR_YELLOW = 0xFFFF00;
	public static int COLOR_WHITE = 0xFFFFFF;
	public static int COLOR_CYAN = 0x00FFFF;
	
	
	public LEDStrip(SensorPort port) {
		i2cPort = port;
		i2cPort.i2cEnable(I2CPort.STANDARD_MODE);
		

	}
	
	public void off() {
		setRGB(0);
	}

	public void setRGB(int color) {
		setRGB((color >> 16) & 0xFF, ((color >> 8) & 0xFF), color & 0xFF);
	}
	public void fadeToRGB(int color) {
		fadeToRGB((color >> 16) & 0xFF, ((color >> 8) & 0xFF), color & 0xFF);
	}

	public void setRGB(int r, int g, int b) {
		byte data[] = { 0x6e, (byte) r, (byte) g, (byte) b };
		i2cPort.i2cTransaction(0x00, data, 0, 4, null, 0, 0);
	}

	public void fadeToRGB(int r, int g, int b) {
		byte data[] = { 0x63, (byte) r, (byte) g, (byte) b };
		i2cPort.i2cTransaction(0x00, data, 0, 4, null, 0, 0);
	}

}
