import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList } from 'react-native';
import { Button, ListItem } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { styleDebug, mockupTicket } from '../helpers';

async function retrieveTicket(id) {
  let responseJson = null;
  try {
    const response = await fetch(`http://127.0.0.1:5001/get_ticket/${id}`);
    if (response.status === 200) {
      responseJson = await response.json();
      alert(`Success: ${response.status} ${response.statusText || ''}`);
    }
    alert(`Error: ${response.status} ${response.statusText || ''}`);
    return responseJson;
  } catch (error) {
    alert(error);
    return responseJson;
  }
}

export default function TicketViewContainer(props) {
  const [ticketId, setTicketId] = useState(props.navigation.getParam('_id', null));
  const [elements, setElements] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      console.log('fetching data...');
      let elems = {};
      if (ticketId) {
        elems = await retrieveTicket(ticketId);
      } else {
        elems = props.navigation.getParam('elements', {});
      }
      elems = Object.values(elems);
      setElements(elems);
    };

    fetchData();
  }, []);

  const handlePressedLine = index => {
    Alert.prompt(
      'Edit',
      'Correct the line as you see fit',
      itemValue => {
        const arr = [...elements];
        arr[index] = itemValue;
        setElements(arr);
      },
      'plain-text',
      elements[index],
      'numeric'
    );
  };

  const arr2obj = arr => {
    const obj = {};
    arr.forEach((e, i) => {
      obj[`line${i}`] = e;
    });
    return obj;
  };

  async function handleConfirmPress() {
    let responseJson = null;
    const url = ticketId
      ? 'http://127.0.0.1:5001/update_ticket'
      : 'http://127.0.0.1:5001/add_ticket';
    const body = ticketId
      ? { _id: ticketId, ticket: arr2obj(elements) }
      : { ticket: arr2obj(elements) };
    try {
      console.log(`${ticketId ? 'updating ' : 'adding '}${JSON.stringify(body)}`);
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      if (response.status === 200) {
        responseJson = await response.json();
        alert(`Success: ${response.status} ${response.statusText || ''}`);
      }
      alert(`Error: ${response.status} ${response.statusText || ''}`);
      return responseJson;
    } catch (error) {
      alert(error);
      return responseJson;
    }
  }

  return (
    <View style={styles.container}>
      <FlatList
        style={styles.list}
        data={elements}
        renderItem={({ item, index }) => {
          return (
            <ListItem
              title={item}
              containerStyle={{ padding: 5 }}
              onPress={() => handlePressedLine(index)}
            />
          );
        }}
        keyExtractor={(item, index) => index.toString()}
      />
      <Button title="Save" style={styles.button} onPress={handleConfirmPress} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    ...styleDebug('red'),
    flex: 1,
  },
  list: {
    ...styleDebug('darkgreen'),
  },
});

TicketViewContainer.propTypes = {};
TicketViewContainer.defaultProps = {};
