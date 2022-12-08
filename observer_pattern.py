# import librarys
from __future__ import annotations
import json
import time
from random import randrange
import datetime
import calendar
import requests
#import schedule
import krakenex
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import List


class ObservableParameter(ABC):
    """Die abstrakte Klasse ObservableParamenter beschreibt Methoden die
    zwingend von Parametern übernommen werden müssen.
    """

    def __init__(self):
        """Konstruktor, der eine leere Liste erstellt, in der die Observer
        gelistet sind.
        """
        self.observers: List[Observer] = []

    @property
    def countObservers(self):
        """Gibt die Anzahl der Beobachter eines Parameters aus."""
        return len(self.observers)

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Observer wird der Liste hinzugefügt.

        args:
        observer (Observer): Beobachter der hinzugefügt werden soll.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Observer wird von der Liste entfernt.

        args:
        observer (Observer): Beobachter der entfernt werden soll.
        """
        pass

    @abstractmethod
    def fireUpdate(self, value) -> None:
        """Benachrichtigung aller Beobachter über den neuen Wert des Parameters.

        args:
        value (float): Der Wert, der geupdatet wird.
        """
        pass


class Price(ObservableParameter):
    """Die Klasse Price erbt von Observable Parameter und beschreibt einen
    beobachtbaren Parameter innerhalb der Trading-Bot-Software.
    """
    tradingPair: tuple = None
    value: float = None
    name: str = None

    def __init__(self, tradingPair, name):
        """Konstruktor, der Werte bei der Objekterstellung zuweist.

        args:
        tradingPair (tuple): Tradingpaar, das beobachtet werden soll.
        name (str): Name des Objekts.
        """
        super().__init__()  # Deklariert obeservers Liste
        self.tradingPair = tradingPair
        self.name = name

    def attach(self, observer: Observer) -> None:
        """Observer wird der Liste hinzugefügt.

        args:
        observer (Observer): Beobachter der hinzugefügt werden soll.
        """
        self.observers.append(observer)
        print('{param} parameter hat {analyse} als Observer hinzugefügt.'\
            .format(param = self.name, analyse = observer.name))

    def detach(self, observer: Observer) -> None:
        """Observer wird von der Liste entfernt.

        args:
        observer (Observer): Beobachter der entfernt werden soll.
        """
        self.observers.remove(observer)
        print('{param} parameter hat {analyse} als Observer entfernt.'\
            .format(param = self.name, analyse = observer.name))

    def fireUpdate(self, value) -> None:
        """Benachrichtigung aller Beobachter über den neuen Wert des Parameters.

        args:
        value (float): Der Wert, der geupdatet wird.
        """
        print("Observer werden benachrichtigt...\n")
        for observer in self.observers:
            observer.update(self, value)


class Volume(ObservableParameter):
    """Die Klasse Volume erbt von Observable Parameter und beschreibt einen
    beobachtbaren Parameter innerhalb der Trading-Bot-Software.
    """
    tradingPair: tuple = None
    value: float = None
    name: str = None

    def __init__(self, tradingPair, name):
        """Konstruktor, der Werte bei der Objekterstellung zuweist.

        args:
        tradingPair (tuple): Tradingpaar, das beobachtet werden soll.
        name (str): Name des Objekts.
        """
        super().__init__()  # Deklariert obeservers Liste
        self.tradingPair = tradingPair
        self.name = name

    def attach(self, observer: Observer) -> None:
        """Observer wird der Liste hinzugefügt.

        args:
        observer (Observer): Beobachter der hinzugefügt werden soll.
        """
        self.observers.append(observer)
        print('{param} parameter hat {analyse} als Observer hinzugefügt.'\
            .format(param = self.name, analyse = observer.name))

    def detach(self, observer: Observer) -> None:
        """Observer wird von der Liste entfernt.

        args:
        observer (Observer): Beobachter der entfernt werden soll.
        """
        self.observers.remove(observer)
        print('{param} parameter hat {analyse} als Observer entfernt.'\
            .format(param = self.name, analyse = observer.name))

    def fireUpdate(self, value) -> None:
        """Benachrichtigung aller Beobachter über den neuen Wert des Parameters.

        args:
        value (float): Der Wert, der geupdatet wird.
        """
        print("Observer werden benachrichtigt...\n")
        for observer in self.observers:
            observer.update(self, value)


class Observer(ABC):
    """
    Abstrakte Klasse, die Methoden beschreibt, die zwingend von Beobachtern
    übernommen werden müssen.
    """

    @abstractmethod
    def update(self, observable: ObservableParameter, value) -> None:
        """Methode zum updaten der beobachteten Werte.

        args:
        observable (ObservableParameter): Parameter, der beobachtet wird.
        value: Neuer Parameter-Wert
        """
        pass


class Analyse(Observer):
    """"Die Klasse Analyse beobachtet die Parameter Werte und trifft Trading-
    Entscheidungen.
    """
    name = None
    paramValues = pd.DataFrame()

    def __init__(self, id, tradingStrategie):
        """Konstruktor, der Werte bei der Objekterstellung zuweist.

        args:
        id (int): ID der Analyse
        tradingStrategie (TradingStrategie): Tradingstrategie in Form von
        Parameter- und Grenzwertlisten.
        """
        # Erstellt Spalten für das Dataframe in der die Parameter sowie
        # die entsprechenden Grenzwerte aus der Strategie und Live-Werte
        # der Parameter geführt werden
        self.name = 'analyse_' + str(id)
        self.paramValues = tradingStrategie.paramLimits.copy()
        self.paramValues['liveValue'] = np.nan

        # abonniert die von der Trading-Strategie übergebenen Parameter
        for i in self.paramValues['parameter_obj']:
            i.attach(self)
        print('\n{analyse} hat die Parameter der {strat} erfolgreich ' \
            'abonniert...\n'.format(analyse = self.name, strat = \
            tradingStrategie.name))

    def update(self, observable: ObservableParameter, value):
        """Methode zum updaten der beobachteten Werte.

        args:
        observable (ObservableParameter): Parameter, der beobachtet wird.
        value: Neuer Parameter-Wert
        """
        # Holt den Index der relevanten Zeile, und ändert den Parameter-Wert
        idx = self.paramValues.index[self.paramValues['parameter_obj'] \
            == observable]
        self.paramValues.loc[idx[0], 'liveValue'] = value
        print(self.name + ' aktualisiert {param} Parameter auf Wert {val}...'\
            .format(param = observable.name, val = observable.value))
        print('parameter liste {}'.format(self.name))
        print(self.paramValues.head())
        print('\n')

        # Lässt den aktualisierten Parameter direkt in die Analyse einfließen
        # und öffnet bzw. schließt ggf. Positionen
        if (value <= self.paramValues.loc[idx[0], 'limitValue']):
            print("{analyse}: Aufgrund des neuen {param} Wertes, wird eine " \
                "neue Position eröffnet!\n".format(analyse = self.name, \
                param = observable.name))
            print('>>>>>>>>> OPEN <<<<<<<<<\n\n')
        if (value > self.paramValues.loc[idx[0], 'limitValue']):
            print("{analyse}: Aufgrund des neuen {param} Wertes, wird eine " \
                "Position geschlossen!\n".format(analyse = self.name, \
                param = observable.name))
            print('>>>>>>>>> CLOSE <<<<<<<<<\n\n')


class TradingStrategie():
    """Die Klasse Tradingstrategie definiert die Parameter, auf die von der
    Analyse zugegriffen werden kann.
    """
    # Kreiert ein neues, leeres Dataframe für die Parameter-Werte und -Limits
    paramLimits = pd.DataFrame(columns = ['parameter_obj', 'parameter_name', \
        'limitValue'])
    name = None

    def __init__(self, name):
        """Konstruktor, der Werten bei der Objekterstellung zuweist.

        args:
        name (str): Name des Objekts.
        """
        self.name = name

    def addParam(self, parameter: ObservableParameter, limitValue) -> None:
        """Neue Parameter und entsprechende Grenzwerte werden zur Strategie
        hinzugefügt.

        args:
        parameter (ObservableParameter): Parameter, der beobachtet werden soll.
        limitValue (float): Grenzwert des Parameters für Tradingentscheidung.
        """
        data = {'parameter_obj': [parameter], 'parameter_name': \
            [parameter.name], 'limitValue': [limitValue]}
        new_row = pd.DataFrame(data)
        self.paramLimits = self.paramLimits.append(new_row, ignore_index=True)

        print("{strat}: Neuer Parameter {param} mit Limit Value {limval} "\
            "erfolgreich zu {strategie} hinzugefügt!\nNeue Parameter Liste:"\
            .format(strat = self.name, param = parameter.name, limval = \
            limitValue, strategie = self.name))
        print(self.paramLimits.head())
        print('\n')

    def removeParam(self, parameter: ObservableParameter) -> None:
        """Übergebene Parameter werden aus der Strategie entfernt.

        args:
        parameter (ObservableParameter): Parameter, der entfernt werden soll.
        """
        # Holt Index der relevanten Zeile und entfernt Parameter.
        idx = self.paramLimits.index[self.paramLimits['parameter_obj'] \
            == parameter]
        self.paramLimits = self.paramLimits.drop(idx)

        print("Parameter {param} erfolgreich aus {strategie} entfernt!\n". \
            format(param = parameter.name, strategie = self.name))
        print("Neue Parameter Liste:")
        print(self.paramLimits.head())
        print('\n')


def value_Listener(df, observable_objects):
    """Hier werden die Live Values der observierten Parameter beim Observer
    aktualisiert und fließen in die laufende Analyse ein.

    args:
    observable_objects (List): Liste mit den beobachteten Parametern.
    df (DataFrame): Tabelle mit aktuellen Werten eines Parameter.
    """
    # Iteriere durch alle Objekte, die beobachtet werden können
    for o in observable_objects:
        if(df.iloc[len(df)-1][o.name]-df.iloc[len(df)-2][o.name] != 0):
            o.value = df.iloc[len(df)-1][o.name]
            print('{observable} hat sich auf {val} aktualisiert!'\
                .format(observable = o.name, val = o.value))
            o.fireUpdate(o.value)


def get_data(pair, since):
    """Hier werden die Live-Daten aus der Kraken-API geladen.

    args:
    pair (tuple): Beobachtetes Trading Paar.
    since (str): Datum, ab Beobachtung.

    returns:
    crypt_data (List [str]): Kurswerte
    """
    crypt_data = api.query_public(
        'OHLC',
        data={'pair':pair, 'since':since})['result'][pair]
    return crypt_data


def update_live_data(df, since):
    """Hier wird die Tabelle mit den Live-Daten geupdatet.

    args:
    df (DataFrame): Tabelle mit der zeitlichen Abfolge von Werten eines
        Parameters.
    since (str): Datum, ab Beobachtung.
    """
    data = get_data(pair[0]+pair[1], since)
    column_names = ['unixtimestamp', 'open', 'high', 'low', 'price', 'vwap',
                    'volume', 'count']
    new_live_data = pd.DataFrame(data, columns = column_names)
    new_live_data = new_live_data.astype({'open': 'float64', 'high': 'float64',
                                          'low': 'float64', 'price': 'float64',
                                          'vwap': 'float64',
                                          'volume': 'float64'})
    df = df.append(new_live_data, ignore_index=True)
    print(df.tail())
    print()
    return df


def create_Strategy(price: ObservableParameter, volume: ObservableParameter):
    """Erzeugt beispielhaft zwei vom User festgelegte Trading Strategien, die
    jeweils unterschiedliche Parameterkombinationen und Grenzwerte einbeziehen.

    args:
    price (ObservableParameter)
    volume (ObservableParameter)
    """
    name_1 = "trading_strategie_1"
    name_2 = "trading_strategie_2"

    # Erzeugt die erste Trading-Strategie mit den Parametern Price und
    # Trading-Volume und den entsprechenden Grenzwerten 1600 und 20
    print('Erstelle Trading Strategie 1...')
    tradingStrategie_1 = TradingStrategie(name_1)
    tradingStrategie_1.addParam(price, 1600.0)
    tradingStrategie_1.addParam(volume, 100)

    # Erzeugt die zweite Trading-Strategie mit den Parametern Price und
    # Trading-Volume und den entsprechenden Grenzwerten 1600 und 20
    print('Erstelle Trading Strategie 2...')
    tradingStrategie_2 = TradingStrategie(name_2)
    tradingStrategie_2.addParam(price, 1590.0)
    tradingStrategie_2.addParam(volume, 50)
    return tradingStrategie_1, tradingStrategie_2


if __name__ == '__main__':
    """Verbindet sich mit der Kraken API und erstellt ein Dataframe in dem
    Marktdaten für das Währungspaar Ethereum-USDollar historisch gespeichert
    werden können. Es werden Observable sowie Observer Objekte erzeugt und mit
    Beispielwerten initialisiert. Die Observer abonnieren ausgewählte
    Observables. Alle fünf Sekunden werden die neuen Echtzeit-Daten über die
    API abgefragt und im Dataframe gespeichert. Falls sich die Werte geändert
    haben, aktualisieren sich die Parameter Echtzeit-Werte.
    """
    api = krakenex.API()
    api.load_key('./kraken.key')
    sleeping_time = 5
    pair = ("XETH", "ZUSD")

    # Globaler Datenbank Dataframe, um historische Marktdaten zu speichern.
    df = pd.DataFrame({'unixtimestamp': 0, 'open': 0.0, 'high': 0.0, 'low': 0.0,
                       'price': 0.0, 'vwap': 0.0, 'volume': 0.0, 'count': 0},
                       index=[0])
    id_1 = 1
    id_2 = 2

    # Kreiert die Objekte aller möglichen Parameter
    observable_price = Price(pair, 'price')
    observable_volume = Volume(pair, 'volume')
    observable_objects = [observable_price, observable_volume]

    # Simuliert die Erstellung zweier Trading Strategien durch den Anwender
    # Es werden Strategien erzeugt, die für ausgewählte Parameter
    # Limit Values festlegt, die von der Analyse berücksichtigt werden
    print('\nErstelle Trading Strategien...\n')
    tradingStrategien = create_Strategy(observable_price, observable_volume)
    tradingStrategie_1 = tradingStrategien[0]
    tradingStrategie_2 = tradingStrategien[1]
    print('Trading Strategien erfolgreich erstellt!\n')
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"\
        ">>>>>>>>>>>>>>>>>>\n")

    # Simuliert das nachträgliche entfernen eines Parameters aus
    # der Trading Strategie durch den Anwender
    print('Update Trading Strategien...\n')
    tradingStrategie_2.removeParam(observable_volume)
    print('Trading Strategien erfolgreich geupdated!\n')

    # Erzeugt neue Objekte der Klasse Analyse und übergibt die
    # Trading-Strategien als Parameter
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"\
        ">>>>>>>>>>>>>>>>>>\n")
    print('Übergebe Trading Strategien an die Analyse...\n')
    analyse_1 = Analyse(id_1, tradingStrategie_1)
    analyse_2 = Analyse(id_2, tradingStrategie_2)
    print('Relevante Parameter wurden erfolgreich von der Analyse abonniert!\n')
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"\
        ">>>>>>>>>>>>>>>>>>\n")

    # Gibt eine Übersicht über Beobachter und beobachtete Objekte
    print('Übersicht über die Observer und observierten Objekte:\n')
    print('Observable price hat {} observer:'\
        .format(observable_price.countObservers))
    for i in observable_price.observers:
        print(i.name)
    print()
    print('Observable volume hat {} observer:'\
        .format(observable_volume.countObservers))
    for i in observable_volume.observers:
        print(i.name)
    print()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"\
        ">>>>>>>>>>>>>>>>>>\n")
    print("Starte Data Stream von der Kraken API und speichere Werte im "\
        "globalen Dataframe...\n")

    while 1:
        """Startet die Endlosschleife, in der alle fünf Sekunden neue Daten von
        der API geladen und gespeichert werden. Dabei wird bei jeder Iteration
        geprüft, ob sich einer der Parameter geändert hat und falls dies der
        Fall ist, die Parameter-Werte aktualisiert und alle Beobachter dieses
        Parameters benachrichtigt.
        """

        # Definiert das Zeitintervall innerhalb dessen die API-Daten abgefragt
        # werden
        since = str(int(time.time()-60))

        # Aktualisiere Dataframe
        df = update_live_data(df, since)

        # prüfe, ob sich für einen Parameter der Live Wert zur vorherigen
        # Abfrage geändert hat
        # und aktualisiere den Wert im Parameter Objekt ggf.
        value_Listener(df, observable_objects)

        print('Warte auf erneuten API Zugriff...\n')
        time.sleep(sleeping_time)
