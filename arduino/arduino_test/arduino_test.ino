int interruptor=2;
int ignition=3;

void setup() {
  // put your setup code here, to run once:
  pinMode(interruptor,INPUT);
  digitalWrite(interruptor,HIGH);
  attachInterrupt(0,ignite,RISING);  
  pinMode(ignition,OUTPUT);
  digitalWrite(ignition,LOW);
}

void ignite() {
  digitalWrite(ignition,HIGH);
  delay(100);
}
void loop() {
  // put your main code here, to run repeatedly:
  //delay(100);
  digitalWrite(ignition,LOW);
}
