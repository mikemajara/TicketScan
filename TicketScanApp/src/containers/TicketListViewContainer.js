import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList, ActivityIndicator, Modal } from 'react-native';
import { Button, ListItem, Icon } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { iOSColors } from 'react-native-typography';
import AppleStyleSwipeableRow from './AppleStyleSwipeableRow';
import TicketListItemComponent from '../components/TicketListItemComponent';
import CompanyRepository from '../repository/CompanyRepository';
import TicketRepository from '../repository/TicketRepository';

import { styleDebug, mockupTicket, getMockupTicket } from '../helpers';
import LoadingComponent from '../components/LoadingComponent';

export default function TicketViewContainer(props) {

  const [elements, setElements] = useState(null);
  const [loading, setLoading] = useState(false);
  const ticketRepository = new TicketRepository();

  useEffect(() => {
    const fetchTickets = async () => {
      setLoading(true);
      let response = [];
      try {
        response = await ticketRepository.findAll();
        setElements(response);

        // TODO: REMOVE TRACE
        console.log(`${new Date().toISOString()} - TicketListViewContainer:36:elements`);
        console.log(elements);
        // ^^^^^ REMOVE TRACE

        setLoading(false);
      } catch (error) {
        setLoading(false);
      }
    };

    fetchTickets();
  }, []);

  const handlePressedLine = async _id => {
    // TODO: Ticket pressed disabled.
    props.navigation.navigate('TicketView', { _id });
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
          // console.log(item, index);
          return (
            <AppleStyleSwipeableRow
              deleteContent={<Icon type="ionicon" name="ios-trash" color="white" size={35} />}
              flagContent={<Icon type="ionicon" name="ios-star" color="white" size={35} />}>
              <TicketListItemComponent
                // units={item.units}
                companyName={`${item.company.name}`}
                date={item.datetime}
                ticket={item}
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
                onPress={() => {
                  console.log('handling press');
                  handlePressedLine(item._id);
                }}
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
