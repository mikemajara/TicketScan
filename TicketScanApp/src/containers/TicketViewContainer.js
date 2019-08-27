import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList } from 'react-native';
import { Button, ListItem } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { styleDebug, mockupTicket } from '../helpers';

export default function TicketViewContainer(props) {
  const [elements, setElements] = useState(
    Object.values(props.navigation.getParam('elements', {}))
  );

  const handlePressedLine = index => {
    Alert.prompt(
      'Number of digits per operation',
      'How many digits do you want the operands to have in your training?',
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
      obj[`linea${i}`] = e;
    });
    return obj;
  };

  async function handleConfirmPress() {
    let responseJson = null;
    try {
      const response = await fetch('http://127.0.0.1:5001/add_ticket', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticket: arr2obj(elements) }),
      });
      if (response.status === 200) {
        responseJson = await response.json();
        console.log(
          `${new Date().toISOString()} - TicketViewContainer:handleConfirmPress:responseJson`
        );
        console.log(responseJson);
        alert(`Success: ${response.status} ${response.statusText || ''}`);
        return responseJson;
      }
      alert(`Error: ${response.status} ${response.statusText || ''}`);
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
      <Button title="Confirm" style={styles.button} onPress={handleConfirmPress} />
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
