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
import { iOSColors } from 'react-native-typography';
import { Icon } from 'react-native-elements';

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
    // where is the border comming from? 
    cardStyle: {
      // backgroundColor: iOSColors.lightGray,
      // margin: 10
      // borderBottomWidth: 0,
    }
  }
);

export const TicketListStackNavigator = createStackNavigator(
  {
    TicketList: {
      screen: TicketListViewContainer,
    },
    TicketView: {
      screen: TicketViewContainer,
    },
  },
  {
    initialRouteName: 'TicketView',
  }
);

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
    initialRouteName: 'Scanner',
    defaultNavigationOptions: ({ navigation }) => ({
      tabBarIcon: ({ focused, horizontal, tintColor }) => {
        const { routeName } = navigation.state;
        let iconName, type;
        switch (routeName) {
          case 'Scanner':
            type = 'ionicon'
            iconName = 'ios-qr-scanner';
            break;
          case 'TicketList':
            type = 'font-awesome5'
            iconName = 'receipt';
            break;
          case 'Settings':
            type = 'ionicon'
            iconName = 'ios-cog';
            break;
          default:
            break;
        }
        return (
          <Icon
            iconStyle={{ fontSize: 25 }}
            type={type}
            name={iconName}
            color={focused ? iOSColors.blue : iOSColors.lightGray2}
            size={13}
          />
        );
      },
      headerTintColor: '#fff',
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }),
    tabBarOptions: {
      activeTintColor: iOSColors.blue,
      inactiveTintColor: iOSColors.gray,
      keyboardHidesTabBar: true,
      style: {
        borderTopWidth: 0,
      }
    },
  },
);

const AppContainer = createAppContainer(TabNavigator);

const App = () => {
  return <AppContainer />;
};

export default App;
