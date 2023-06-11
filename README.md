Gulf of Suez Petroleum company (GUPCO) is one of the largest brownfields in Egypt since 1965. The company main concessions are in Ras Shukier field which comprises numerous producer and injector wells. Most of producer wells are gas lift wells with small percent of natural flow and ESP wells. The field has a giant network of offshore/onshore pipelines connecting satellite platforms to central complex platforms for 1) gathering production from connected wells, 2) primary separating gas/fluid streams, 3) compressing gas lift using several huge compressor modules to be injected again in producer wells and 4) testing each well using test separators installed in central complex platforms, from where the fluid stream is then sent to onshore units for secondary separation and processing.

Regular testing of producer wells is a crucial task in the company since most of the wells are producing by the available gas lift in the network. Therefore, wells testing is considered the main key for optimizing injection gas for each well, prioritizing on stream wells, having high oil production per 1 MMSCFD gas lift, in order to maximize the total oil production and calculating company's revenues in accurate way when back allocating daily oil production to each concession. Physical well testing devices used in the field involve complex test separators, portable test separator and multi-phase flow meters. However, testing this enormous number of producer wells using physical devices only is considered one of the major challenges in the field due to the following reasons:

Most of testing separators and pipelines are old and out of services due to technical operating problems.
Logistics and weather difficulties limiting the flexibility of installing/backloading the portable test separator in offshore platforms.
Multi phase flow meter is installed only in main vital platforms due to its high capital/operating cost.
Consequently to overcome the above difficulties, virtual testing techniques, either physics driven or data driven, become a fundamental alternate to other testing techniques. Physics driven model as Prosper and Pipesim software are commonly used for estimating wells fluid rate, but these models have some shortcomings including the relatively long time consumed to build well or entire field network, the high sensitivity of prediction error to input model variables and the uncertainty of the input recorded data.

In this notebook, a new data driven model is introduced to overcome the previous shortcomings of physical and virtual testing methods. The model is based on machine learning/deep learning methods, where the model shows outstanding simplicity and applicability in only few seconds for predicting fluid rate with relatively high accuracy compared to the commonly used methods in the company. The applied steps for building the model are summarized as following:

Analyzing General Energy Equation for fluid mechanics to select the relevant inputs
Filtering the selected inputs according to the availability of actual recorded data
Collecting sample of data from the company database
Testing model performance against data sample
Selecting important features using three different approaches
Collecting new data only for selected features
Exploring the data variables using Exploratory Data Analysis (EDA)
Comparing the results of different machine learning models and selecting the best model.
Optimizing the model by hyperparameters fine tuning
Applying the same data on deep learning model and comparing the results.
