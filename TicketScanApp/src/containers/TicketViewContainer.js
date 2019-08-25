import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Button, Text, FlatList } from 'react-native';
// import { Animated } from 'react-native-reanimated';
import { styleDebug, mockupTicket } from '../helpers';

export default function TicketViewContainer(props) {
  const arr = Object.values(mockupTicket).slice(0, 6);
  const headerItems = [];
  arr.forEach((e, i) => {
    console.log(e);
    headerItems.push(
      <Text style={styles.lineHeaderButton} onPress={() => alert(e)}>
        {e}
      </Text>
    );
  });
  const footerLine = [
    <Text>TOTAL........EUROS: 17,74</Text>,
    <Text>EFECTIVO.....EUROS: 18,00</Text>,
    <Text>DEVOLUCION...EUROS: 0,26</Text>,
  ]
  return (
    <View>
      <View style={styles.header}>{headerItems}</View>
      <FlatList
        style={styles.list}
        data={Object.values(mockupTicket).slice(6, 14)}
        renderItem={({ item, index, section }) => (
          <Text style={styles.lineHeaderButton}>{item}</Text>
        )}
        keyExtractor={(item, index) => index}
      />
      <View style={styles.lineFooterButton}>{footerLine}</View>
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
  footer: {
    ...styleDebug('purple'),
    alignItems: 'center',
  },
  list: {
    ...styleDebug('darkgreen'),
  },
  lineHeaderButton: {
    margin: 0,
    padding: 0,
    color: 'black',
  },
  lineFooterButton: {
    color: 'black',
  },
});

TicketViewContainer.propTypes = {};
TicketViewContainer.defaultProps = {};
