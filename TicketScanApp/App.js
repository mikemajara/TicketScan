/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */
import React from 'react';
import { View } from 'react-native';

import {
  createStackNavigator,
  createBottomTabNavigator,
  createAppContainer,
} from 'react-navigation';
import ScannerViewContainer from './src/containers/ScannerViewContainer';
import TicketViewContainer from './src/containers/TicketViewContainer';
import TicketListViewContainer from './src/containers/TicketListViewContainer';
// import Ionicons from 'react-native-vector-icons/Ionicons';

const dummyComponent = () => {
  return <View />;
};

export const ScannerStackNavigator = createStackNavigator(
  {
    ScannerView: {
      screen: ScannerViewContainer,
    },
    TicketView: {
      screen: TicketViewContainer,
    },
  },
  {
    initialRouteName: 'ScannerView',
  }
);

export const TicketListStackNavigator = createStackNavigator({
  TicketList: {
    screen: TicketListViewContainer,
  },
  TicketView: {
    screen: TicketViewContainer,
  },
});

export const SettingsStackNavigator = createStackNavigator({
  Settings: {
    screen: dummyComponent,
  },
});

export const TabNavigator = createBottomTabNavigator(
  {
    Scanner: {
      screen: ScannerStackNavigator,
    },
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
  return <AppContainer />;
};

export default App;
