import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList } from 'react-native';
import { Button, ListItem } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { styleDebug, mockupTicket } from '../helpers';

export default function TicketViewContainer(props) {
  const [elements, setElements] = useState([]);
  const [loading, setLoading] = useState(true);

  async function getTickets() {
    let responseJson = null;
    try {
      const response = await fetch('http://127.0.0.1:5001/get_all_tickets');
      if (response.status === 200) {
        responseJson = await response.json();
        console.log(
          `${new Date().toISOString()} - TicketViewContainer:handleConfirmPress:responseJson`
        );
        console.log(responseJson);
        alert(`Success: ${response.status} ${response.statusText || ''}`);
      }
      alert(`Error: ${response.status} ${response.statusText || ''}`);
      return responseJson;
    } catch (error) {
      alert(error);
      return responseJson;
    }
  }

  useEffect(async () => {
    setElements(await getTickets());
    setLoading(false);
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

  if (loading) {
    return <View><Text>Loading</Text></View>
  }

  return (
    <View style={styles.container}>
      <FlatList
        style={styles.list}
        data={elements.tickets}
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
