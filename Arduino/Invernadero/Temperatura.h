#ifndef TEMPERATURA_H
#define TEMPERATURA_H

#include <Arduino.h>
#include <DHT.h>

DHT dht(2, DHT11);

bool ventiladorActivo = false;

void iniciarTemperatura() {
  dht.begin();
  digitalWrite(7, HIGH);
  pinMode(7, OUTPUT);
}

float leerTemperatura() {
  return dht.readTemperature();
}

void controlarVentilador(float temperatura) {
  if (isnan(temperatura)) {
    ventiladorActivo = false;
  }
  else if (temperatura >= 30.0) {
    ventiladorActivo = true;
  }
  else if (temperatura <= 28.0) {
    ventiladorActivo = false;
  }

  digitalWrite(7, ventiladorActivo ? LOW : HIGH);
}

#endif
