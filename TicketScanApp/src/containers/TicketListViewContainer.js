import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList, ActivityIndicator, Modal } from 'react-native';
import { Button, ListItem, Icon } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { iOSColors } from 'react-native-typography';
import AppleStyleSwipeableRow from './AppleStyleSwipeableRow';
import TicketListItemComponent from '../components/TicketListItemComponent';

import { styleDebug, mockupTicket, getMockupTicket } from '../helpers';
import LoadingComponent from '../components/LoadingComponent';

export default function TicketViewContainer(props) {
  const [elements, setElements] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTickets = async () => {
      setLoading(true);
      let responseJson = null;
      try {
        const response = await fetch('http://127.0.0.1:5001/get_all_tickets');
        if (response.status === 200) {
          responseJson = await response.json();
          console.log(
            `${new Date().toISOString()} - TicketViewContainer:handleConfirmPress:responseJson`
          );
        }
        // alert(`Result: ${response.status} ${response.statusText || ''}`);
        // setElements(responseJson);
        setElements(
          Array(10)
            .fill(null)
            .map(() => getMockupTicket())
        );
        console.log(`${new Date().toISOString()} - TicketListViewContainer:fetchTickets:elements`);
        console.log(responseJson);
        return responseJson;
      } catch (error) {
        return responseJson;
      } finally {
        setLoading(false);
      }
    };

    fetchTickets();
  }, []);

  const handlePressedLine = _id => {
    // TODO: Ticket pressed disabled.
    // props.navigation.navigate('TicketView', { _id })
    // TODO: get ticket pressed
    // props.navigation.navigate('TicketView', { elements: response })
  };

  const arr2obj = arr => {
    const obj = {};
    arr.forEach((e, i) => {
      obj[`line${i}`] = e;
    });
    return obj;
  };

  const shouldHaveBottomDivider = (idx, len) => Boolean(len - idx - 1);
  const shouldHaveTopDivider = (idx, len) => !idx;

  return (
    <View style={styles.container}>
      {loading && (
        <LoadingComponent
          isLoading={loading}
          loadingText="Getting your tickets from the archive..."
        />
      )}
      <FlatList
        style={styles.list}
        data={elements || []}
        renderItem={({ item, index }) => {
          console.log(item, index);
          return (
            <AppleStyleSwipeableRow
              deleteContent={<Icon type="ionicon" name="ios-trash" color="white" size={35} />}
              flagContent={<Icon type="ionicon" name="ios-star" color="white" size={35} />}>
              <TicketListItemComponent
                // units={item.units}
                name={`${item.company.name} - ${item._id}`}
                bottomDivider={shouldHaveBottomDivider(index, elements.length)}
                topDivider={shouldHaveTopDivider(index, elements.length)}
                leftIcon={
                  <Icon
                    type="ionicon"
                    name="ios-star"
                    color={index % 2 ? iOSColors.yellow : 'transparent'}
                    size={15}
                  />
                }
              />
            </AppleStyleSwipeableRow>
          );
        }}
        keyExtractor={(item, index) => item._id || index.toString()}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    ...styleDebug('red'),
    flex: 1,
  },
  list: {
    ...styleDebug('lightgreen'),
  },
});

TicketViewContainer.propTypes = {};
TicketViewContainer.defaultProps = {};
