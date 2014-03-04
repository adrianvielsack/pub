#define F_CPU 16000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <stdint.h>
#include <avr/interrupt.h>
#include <inttypes.h>
#include "avr/wdt.h"


#define LATCH		PB0
#define LATCH_HIGH	PORTB |= (1<<LATCH);
#define LATCH_LOW	PORTB &=~(1<<LATCH);

#define ENABLE		PB1
#define ENABLE_HIGH	PORTB |=(1<<ENABLE);
#define ENABLE_LOW	PORTB &=~(1<<ENABLE);

volatile unsigned char buffer[512];
volatile unsigned char dim = 0;
int main(void){
	//Initialize IO Ports
	DDRB = (1<<PB0)|(1<<PB3)|(1<<PB5)|(1<<PB1)|(1<<PB2);
	//Turn of the Enable pin to prevent magic smoke in case of Watchdog
	ENABLE_LOW
	DDRC = 0x0F;
	
	//Configure SPI in Fast Mode
	SPCR = (1<<SPE)|(1<<MSTR)|(0<<CPOL)|(1<<DORD);
	SPSR = (1<<SPI2X);
	
	//Init uart to get Data
	UBRR0H = 0;
	UBRR0L = 34;   //57600
	UCSR0A = (1<<U2X0); //Fast Mode
	UCSR0B = (1<<RXEN0)|(1<<TXEN0)|(1<<RXCIE0); //RXEnable, TXEnable, RXInterrupt enable
	
	//Enable Interrupts for receiving data
	sei();
	//Enable Watchdog to prevent magic smoke in case of errors
	wdt_enable(WDTO_30MS);
	
	SPDR = 0;
	int i, n;
	//Display something
	for (i = 0; i < 16; i++)
		buffer[i + 32 * 15] = (1<<(i % 8));
	//Mainloop for drawing	
	while (1) {
		for (i = 0; i < 16; i++) {
			//ENABLE_LOW If we want the display to be dimmed
			if (dim == 1)
				ENABLE_LOW
			//Push out next row
			for (n = 31; n >=0; n--) {
				
				while (!(SPSR & (1<<SPIF))){
					;
				}
				SPDR = ~buffer[n + 32 * i];
			}
			//Reset watchdog
			if (dim == 0)
				ENABLE_LOW
			wdt_reset();
			//Disable Display
			_delay_us(3);
			//Latch out data
			LATCH_HIGH
			LATCH_LOW
			//Set the row
			PORTC = (15 - i);
			//Display Row
			ENABLE_HIGH
			_delay_us(10);
		}
	}

}

volatile unsigned char state = 0;
volatile unsigned int counter = 0;
ISR(USART_RX_vect) {
	//Statemachine for receiving Data
	unsigned char c = UDR0;
	if (state == 1) {
		buffer[counter] = c;
		counter++;
		if (counter < 512)
			return;
		state = 0;
		return;
	}
	if ((c & 0xF0) == 0xA0) {
		dim = c & 0x01;
		state = 1;
		counter = 0;
	}
/*	switch (state) {
		case 0:
			if (c == 0xA0) {
				state = 1;
				counter = 0;
			}
			break;
		case 1:
			buffer[counter] = c;
			counter++;
			if (counter == 512)
				state = 0;
			break;
	}*/
}
