import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Button, Text, FlatList } from 'react-native';
// import { Animated } from 'react-native-reanimated';
import { styleDebug, mockupTicket } from '../helpers';

export default function TicketViewContainer(props) {
  const arr = Object.values(mockupTicket).slice(0, 6);
  const headerItems = [];
  arr.forEach((e, i) => {
    console.log(e)
    headerItems.push(<Text style={styles.lineButton} onPress={() => alert(e)}>{e}</Text>)
  });
  return (
    <View>
      <View style={styles.header}>
        {headerItems}
      </View>
      <FlatList
        style={styles.list}
        data={Object.values(mockupTicket).slice(6)}
        renderItem={({ item, index, section }) => <Button title={item} />}
        keyExtractor={(item, index) => index}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    ...styleDebug('red'),
    flex: 1,
  },
  header: {
    ...styleDebug('blue'),
    alignItems: 'center',
  },
  list: {
    ...styleDebug('darkgreen'),
    marginBottom: 100,
  },
  lineButton: {
    margin: 0,
    padding: 0,
    color: 'black',
  },
});

TicketViewContainer.propTypes = {};
TicketViewContainer.defaultProps = {};
