
/*
  Proyecto: Invernadero Inteligente
  Sistema de ventilacion y riego automatico
  Integracion de modulos y comunicacion con Python
*/

#include <Arduino.h>
#include "Temperatura.h"
#include "Riego.h"

// Variables de monitoreo
float temperatura = 0.0;
int humedad = 0;

void setup() {
  // Comunicacion con Python
  Serial.begin(9600);

  // Inicializacion de los modulos
  iniciarTemperatura();
  iniciarRiego();

  delay(2000);
}

void loop() {

  // Lectura de sensores
  temperatura = leerTemperatura();
  humedad = leerHumedad();

  // Control automatico
  controlarVentilador(temperatura);
  controlarBomba(humedad);

  // Envio de temperatura
  Serial.print(temperatura, 1);
  Serial.print(",");

  // Envio de humedad
  Serial.print(humedad);
  Serial.print(",");

  // Estado del ventilador
  Serial.print(ventiladorActivo ? 1 : 0);
  Serial.print(",");

  // Estado de la bomba
  Serial.println(bombaActiva ? 1 : 0);

  // Actualizacion cada dos segundos
  delay(2000);
}
