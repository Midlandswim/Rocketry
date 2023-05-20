/*
  Data Reciver Test
  Simulates reciving data by printing random
  values to the serial to be read by the GUI program
*/

int logDelay = 250;
String data;
void setup()
{
  Serial.begin(9600);
  Serial.flush();
  Serial.println("\n!!REC_RESET");
}

void loop()
{
  String data = String(millis() / 1000.0);
  for (int i = 0; i < 12; i++)
  {
    data += "," + String(random(10, 100));
  }
  Serial.println(data);
  delay(logDelay);
}