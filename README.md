# README #

Hier werden die Bestandteile des Projekts erläutert und erklärt in welcher Reihenfolge die Skripte ausgeführt werden müssen.

Die nachfolgende Tabelle gibt an welche Dateien als Vorbedingungen für Skripte verfügbar sein müssen (Input),
und welche Datein von einem Skript produziert werden (Output). Dadurch wird die Reihenfolge der Skripte festgelegt.

| Rank | Input                                         | Skript                   | Output                       |
|------|-----------------------------------------------|--------------------------|------------------------------|
| 1    | -                                             | thomann_spider.py        | thomann_reviews_all.csv      |
| 2    | thomann_reviews_all.csv                       | mini_EDA.ipynb           | -                            |
| 3    | thomann_reviews_all.csv                       | preprocessing.ipynb      | enriched_thomann_data.pickle |
| 4    | enriched_thomann_data.pickle                  | baseline_model.ipynb     | -                            |
| 5    | enriched_thomann_data.pickle                  | word2vec.ipynb           | w2v_model.pickle             |
| 6    | enriched_thomann_data.pickle w2v_model.pickle | final_Modelling_v2.ipynb | Models Results               |

Anmerkung: Da die Dateigrößen von *enriched_thomann_data.pickle* und *w2v_model.pickle* die maximale Uploadgröße von Github
überschritten, müssen diese erst durch die entsprechenden Skripte erstellt werden. 

### thomann_spider
Für die Datenbeschaffung ist ein Webscraper in Python mithilfe des Scrapy Paket erstellt worden. Dieser extrahiert Bewertungen von der Webseite [thomann](https://www.thomann.de/de/gitarren_baesse.html).
Das zugehörige Scrapy Projekt befindet sich im Ordner *thomann_spider*. Die aus dem Skript entstandene Datei ist *thomann_reviews_all*.

### mini_EDA.ipynb
In diesem Skript werden die Daten exploriert. Dafür werden teilweise auch Methoden aus create_plots.py benutzt. 

### preprocessing.ipynb
Die Datei thomann_reviews_all bildet den Input für das erste Skript *preprocessing.ipynb*. Hier findet das Negationshandling und klassisches Textpreprocessing statt.

### create_plots.py
Dieses Skript beinhaltet einige Methoden zur grafischen Exploration der Daten.   

### modelling
* final_Modelling_v2.ipynb: hier findet die Implementierung der einzelnen Machine Learning Pipelines statt. Diese kümmern sich um die Vorhersage der Sterne f�r Bewertungen.
* baseline_model.ipynb: erstellt Baseline Vorhersagen um die nachfolgenden Modelle besser evaluieren zu können.
* word2vec.ipynb: dieses Skript trainiert ein Word2Vec Model anhand der vorverarbeiteten Daten.
