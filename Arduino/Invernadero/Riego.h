#ifndef RIEGO_H
#define RIEGO_H

#include <Arduino.h>

bool bombaActiva = false;

// Valores provisionales de calibracion
const int VALOR_SECO = 850;
const int VALOR_HUMEDO = 350;

void iniciarRiego() {
  pinMode(A0, INPUT);
  digitalWrite(8, HIGH);
  pinMode(8, OUTPUT);
}

int leerHumedad() {
  int lectura = analogRead(A0);

  int porcentaje = map(
    lectura,
    VALOR_SECO,
    VALOR_HUMEDO,
    0,
    100
  );

  return constrain(porcentaje, 0, 100);
}

void controlarBomba(int humedad) {
  if (humedad <= 40) {
    bombaActiva = true;
  }
  else if (humedad >= 60) {
    bombaActiva = false;
  }

  digitalWrite(8, bombaActiva ? LOW : HIGH);
}

#endif