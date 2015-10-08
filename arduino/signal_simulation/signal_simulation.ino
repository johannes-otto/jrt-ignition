#include <TimerOne.h>

int led = 13;
int wheel = 2;
int pot = 2;
int shift_up = 9;
int clutch = 4;

int wheelState = LOW;

int go = 2;

int rate = 30000;
int gears[] = {21, 0, 13, 9, 7};
int gi = 0;
int g = gears[gi];

int rounds = 0;

int shifted = LOW;
int ledState = LOW;

int minPot = 400;
int maxPot = 500;
int rateDiv=1;
void blinkLED(void)
{
  rounds += 1;
  if (ledState == LOW) {
    ledState = HIGH;
  } else {
    ledState = LOW;
  }
  if (rounds > 2 * g - 1) {
    wheelState = HIGH;
    rounds = 0;
  }
  else {
    wheelState = LOW;
  }
  digitalWrite(led, ledState);
  digitalWrite(wheel, wheelState);
}

void setup(void)
{
  pinMode(led, OUTPUT);
  pinMode(wheel, OUTPUT);

  pinMode(shift_up, INPUT);
  pinMode(clutch, INPUT);
  digitalWrite(shift_up, HIGH);
  digitalWrite(clutch, HIGH);

  Timer1.initialize(10000);
  Timer1.attachInterrupt(blinkLED);
}


void loop(void)
{
  interrupts();
  if (digitalRead(clutch) == HIGH) {
    if (gears[gi] > 0) {
      int val = analogRead(pot);
      if (val < minPot) {
        minPot = val;
      }
      else if (val > maxPot) {
        maxPot = val;
      }
      rateDiv = map(val, minPot, maxPot, 10, 71);
      //val = val / 35;
      //val = val * 35;
      rate = 300000 / rateDiv;
      g = gears[gi];
      go = g * rate / 30000;
    }
    shifted = LOW;
  }
  else {
    if (digitalRead(shift_up) == LOW) {
      if (shifted == LOW) {
        gi += 1;
        if (gi > 4) {
          gi = 0;
        }
        shifted = HIGH;
      }
    }
    g = go;
    rate = 30000;
  }
  Timer1.setPeriod(rate);
}

