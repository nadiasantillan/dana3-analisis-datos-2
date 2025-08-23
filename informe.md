### Diagrama de Base de Datos
```mermaid
    erDiagram
        USUARIOS {
            string MHDR_KEY
        }
        ALIMENTOS {
            string clave
        }
        USUARIOS}|..|{ALIMENTOS: "Alimentos consumidos por una persona el dia anterior"
```