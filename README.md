# Propuestas de Investigación Grupo I
Se evalúan dos conjuntos de datos considerados interesantes por los miembros del equipo. La razón por la que se analizaron bases de datos es la inexistencia de datos posteriores a 2020 para la encuesta de salud.
## Encuesta Nacional de Nutrición y Salud
### Características

Fuente: Ministerio de Salud y Desarrollo Social de la Nación

La primera ENNyS fue realizada entre los años 2004 y 2005 exclusivamente en la niños mayores de 6  meses a 5 años, embarazadas y mujeres en edad fértil, mientras que la ENNyS 2 realizada en 2018-2019  fue realizada en niños, niñas y adolescentes (NNyA) de ambos sexos de 0 a 17 años, y en adultos de  ambos sexos de 18 años y más.

### Tema de Investigación Propuesto
¿Qué asociaciones existen entre el estado de salud de
los adultos argentinos y variables como edad, sexo,
lugar de residencia, nivel educativo, acceso a la
atención médica y estilo de vida actual?

### Variables
1. Sexo.
1. Edad (en años y agrupada: 18–29, 30–44, 45–59, 60+).
1. Nivel de estudios alcanzado.
1. Región del país (GBA, Centro, NEA, NOA, Cuyo, Patagonia).
1. Tipo de cobertura de salud (pública, obra social, prepaga).
1. Ingreso total del hogar.
1. Peso.
1. Altura.
1. Índice de Masa Corporal (IMC) y clasificación (bajo peso, normal, sobrepeso, obesidad).
1. Perímetro de cintura
1. Presencia declarada de hipertensión, diabetes o colesterol alto.
1. Autopercepción del estado de salud (muy bueno, bueno, regular, malo).

#### Problación Objetivo
Adultos: personas de 18 años o más.

### Documentos
1. [Manual Metodológico](https://datos.gob.ar/dataset/salud-base-datos-2deg-encuesta-nacional-nutricion-salud-ennys2-2018-2019/archivo/salud_d5c86f64-624e-49ef-88e1-9ce62c1d184e)
1. [Encuesta Nacional de Nutrición y Salud, Resumen ejecutivo.](https://cesni-biblioteca.org/wp-content/uploads/2019/10/0000001565cnt-ennys2_resumen-ejecutivo-20191.pdf)
1. [Microdatos](https://datos.gob.ar/dataset/salud-base-datos-2deg-encuesta-nacional-nutricion-salud-ennys2-2018-2019)
### Estudios Existentes
1. Organización Panamericana de la Salud.(2019).[Las ENT de un vistazo: Mortalidad de las enfermedades no transmisibles y prevalencia de sus factores de riesgo en la Región de las Américas](https://iris.paho.org/handle/10665.2/51752)
## Encuesta Nacional de Uso del Tiempo
### Características

Fuente: INDEC

Períodos disponibles: 2013 (no contiene las mismas variables basada en la EAHU/EPH 2013) y 2021

El conjunto de datos se compone de 3 bases de datos: personas entrevistadas, miembros del hogar y diario de uso del tiempo de la persona entrevistada.

### Tema de Investigación Propuesto
 
¿Quienes realizan las tareas de cuidado no pagas? ¿Qué caracteristicas tienen los dadores y demandantes de cuidado?

#### Problación Objetivo
Los sujetos que respondieron la encuesta y que no son demandantes de cuidado y que cuidan a personas dentro del hogar, en hogares con personas con demandantes de cuidado.

#### Variables
1. Genero
1. Edad
1. Parentesco con el jefe de hogar
1. Nivel Educativo
1. CANT_MIEMBROS_HOGAR
1. CANT_PERSONASHASTA13 
1. CANT_PERSONAS14A64
1. CANT_PERSONAS65YMAS
1. CANT_DEMANDANTES_TOTAL 
1. CANT_DEMANDANTES_14A64
1. CANT_DEMANDANTES_65YMAS
1. MAYORESACARGO_TOTAL
1. MAYORES_OTROHOGAR
1. MAYORES_GERIATRICO
1. MAYORES_CUIDADO_PAGO
1. ID
1. N_MIEMBRO
1. N_FILA
1. ACTIVIDAD_HORA
1. ACTIVIDAD_MINUTO
1. ACTIVIDAD_1
1. ACTIVIDAD_2
1. ACTIVIDAD_3

Los registros dentro del alcance serían aquellos en los que ACTIVIDAD_1, ACTIVIDAD_2 y/o ACTIVIDAD_3 tienen valor:
|Código|Descripción|
|----:|----------------------------------------------------------------|
|421 |Cuidados personales y apoyo a miembros del hogar de 14 a 64 años|
|422 |Cuidado temporal de salud a miembros del hogar de 14 a 64 años|
|423|Acompañamiento y traslados a miembros del hogar de 14 a 64 años|
|429|Otras actividades de cuidado y apoyo a miembros del hogar de 14 a 64 años|
|431|Cuidados personales y apoyo a miembros del hogar de 65 años y más|
|432|Cuidado temporal de salud a miembros del hogar de 65 años y más|
|433|Acompañamiento y traslados a miembros del hogar de 65 años y más|
|439|Otras actividades de cuidado y apoyo a miembros del hogar de 65 años y más|
|441|Cuidados personales y apoyo a miembros del hogar con discapacidad o dependencia permanente|
|442|Cuidado de salud a miembros del hogar con discapacidad|
|443|Acompañamiento y traslado a algún lugar a miembros del hogar con discapacidad|
|449|Otras actividades de cuidado a miembros del hogar con discapacidad|

#### Valor Agregado de la Investigación Propuesta

Describir el tiempo que demanda el cuidado de personas mayores de 14 años en nuestro país y quienes cuidan a esas personas.

### Documentos

1. [Manual de uso ENUT 2021](https://www.indec.gob.ar/ftp/cuadros/menusuperior/enut/enut2021_manual_uso_base.pdf)

### Estudios Existentes
1. INDEC. (2022). [Encuesta Nacional de Uso del Tiempo 2021](https://www.indec.gob.ar/ftp/cuadros/sociedad/enut_2021_resultados_definitivos.pdf). INDEC

1. Charmes, J. (2019). [The Unpaid Care Work and
the Labour Market. An analysis
of time use data based on
the latest World Compilation
of Time-use Surveys](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@dgreports/@gender/documents/publication/wcms_732791.pdf).  Organzación Internacional del Trabajo.

### Preguntas

¿La encuesta de 2021 está relacionada con la EPH 2021?

### Desventajas del conjunto de datos
1. No se pueden tomar muestras apareadas debido a la existencia de datos de 2021 solamente.
