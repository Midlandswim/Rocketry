/*
  Data Reciver

  Recives telemetry from a model rocket's transmitter,
  and prints it to the serial output to be read by
  a Python program which will display it in a GUI  
*/

// Data recived from the serial
String recivedData;

void setup()
{
    // Begin serial and wait until it is ready
    Serial.begin(9600);
    while (!Serial);
}

void loop()
{
    // While serial is available
    while (Serial.available() > 0)
    {
        // Read until a closing >
        recivedData = Serial.readStringUntil('>');
        // If the first char is an opening <
        if (recivedData[0] == '<')
        {
            // Write the content to the serial
            Serial.println(recivedData.substring(1));
        }
    }
}