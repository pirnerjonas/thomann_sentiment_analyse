# README #

This README would normally document whatever steps are necessary to get your application up and running.

\begin{table}[]
\centering
\caption{}
\label{undefined}
\begin{tabular}{llll}
\textbf{Rank} & \textbf{Input} & \textbf{Skript} & \textbf{Output} \\
1 & - & \textbf{thomann\_spider.py} & thomann\_reviews\_all.csv \\
2 & thomann\_reviews\_all.csv & \textbf{mini\_EDA.ipynb} & - \\
3 & thomann\_reviews\_all.csv & \textbf{preprocessing.ipynb} & enriched\_thomann\_data.pickle \\
4 & enriched\_thomann\_data.pickle & \textbf{baseline\_model.ipynb} & - \\
5 & enriched\_thomann\_data.pickle & \textbf{word2vec.ipynb} & w2v\_model.pickle \\
6 & \begin{tabular}[c]{@{}l@{}}enriched\_thomann\_data.pickle\\ w2v\_model.pickle\end{tabular} & \textbf{final\_Modelling\_v2.ipynb} & \begin{tabular}[c]{@{}l@{}}Models\\ Results\end{tabular}
\end{tabular}
\end{table}

Anmerkung:
Die Dateien w2v_model.pickle und enriched_thomann_data.pickle mussten wegen ihrer Dateigröße komprimiert werden. Sie werden im Archiv *pickles.7z* zusammengefasst.

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
