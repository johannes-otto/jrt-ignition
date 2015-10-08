#include <TimerOne.h>
int led=5;
int ledState = LOW;
void blinkLED(void)
{
  if (ledState == LOW) {
    ledState = HIGH;
  } else {
    ledState = LOW;
  }
  digitalWrite(led, ledState);
}

void setup(void)
{
  pinMode(led, OUTPUT);
  Timer1.initialize(1000000);
  Timer1.attachInterrupt(blinkLED);
}


void loop(void)
{
  interrupts();
}

