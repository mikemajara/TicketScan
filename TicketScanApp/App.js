/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, { Fragment } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
} from 'react-native';

import {
  Header,
  LearnMoreLinks,
  Colors,
  DebugInstructions,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';
import {
  createStackNavigator,
  createBottomTabNavigator,
  createAppContainer,
} from 'react-navigation';
// import Ionicons from 'react-native-vector-icons/Ionicons';

const dummyComponent = () => {
  return <View />;
};

export const TicketListStackNavigator = createStackNavigator(
  {
    TicketList: {
      screen: dummyComponent,
    },
  }
);

export const SettingsStackNavigator = createStackNavigator(
  {
    Settings: {
      screen: dummyComponent,
    },
  }
);

export const TabNavigator = createBottomTabNavigator(
  {
    TicketList: {
      screen: TicketListStackNavigator,
    },
    Settings: {
      screen: SettingsStackNavigator,
    },
  },
  {
    initialRouteName: 'TicketList',
  },
);

const AppContainer = createAppContainer(TabNavigator);

const App = () => {
  return (
    <AppContainer />
  );
};

export default App;
