import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList, ActivityIndicator, Modal } from 'react-native';
import { Button, ListItem } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { iOSColors } from 'react-native-typography';


import { styleDebug, mockupTicket } from '../helpers';
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
        setElements(responseJson);
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
    props.navigation.navigate('TicketView', { _id })
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

  return (

    <View style={styles.container}>
      {loading && (
        <LoadingComponent
          isLoading={loading}
          loadingText="Getting your tickets from the archive..."
        />)
      }
      <FlatList
        style={styles.list}
        data={elements ? elements.tickets : []}
        renderItem={({ item, index }) => {
          return (
            <ListItem
              title={item._id}
              containerStyle={{ padding: 5 }}
              onPress={() => handlePressedLine(item._id)}
            />
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
