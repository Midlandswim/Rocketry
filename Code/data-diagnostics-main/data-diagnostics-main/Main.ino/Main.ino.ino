void setup()
{
  Serial.begin(9600);
  Serial.println("\n\nRocket Startup");
  Serial.println("-------------------------");
  Serial.println("**Initializing Sensors**");
  sensorInit();
}

void loop()
{
}

void sensorInit()
{
  if (altimeterInit() && gyroInit() && camInit())
  {
    Serial.println("**All Sensors Initialized**\n");
  }
  else
  {
    Serial.println("**Error initializing sensor(s), execution of program is being terminated**\n");
    while (1)
      ;
  }
}

bool altimeterInit()
{
  if (true)
  {
    Serial.println("[OK] Altimeter Initialized");
  }
  else
  {
    Serial.println("[ERROR] Altimeter not Initialized!");
    return false;
  }

  return true;
}

bool gyroInit()
{
  if (true)
  {
    Serial.println("[OK] Gyroscope Initialized");
  }
  else
  {
    Serial.println("[ERROR] Gyroscope not Initialized!");
    return false;
  }

  return true;
}

bool camInit()
{
  if (false)
  {
    Serial.println("[OK] Camera Initialized");
  }
  else
  {
    Serial.println("[ERROR] Camera not Initialized!");
    return false;
  }

  return true;
}
