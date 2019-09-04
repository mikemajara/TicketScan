import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList } from 'react-native';
import { Button, ListItem } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { iOSUIKit, iOSColors } from 'react-native-typography';
import { Icon } from 'react-native-elements';
import Entypo from 'react-native-vector-icons/Entypo';
import { styleDebug, mockupTicket } from '../helpers';
import Ticket from '../model/Ticket';
import Store from '../model/Store';
import TicketLine from '../model/TicketLine';
import CardComponent from '../components/CardComponent';


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
  // Store constructor(company, country, city, address, phone, id) {
  // TicketLine constructor(quantity, weight, price, name, readableName, id, altCodes) {
  // Ticket constructor(store, datetime, proprietaryCodes, paymentMethod, total, returned, ticketLines) {
  const store = new Store(
    'Mercadona',
    'Spain',
    'Murcia',
    'Floridablanca, 4',
    '+34 968227166',
    'A-46103834'
  );
  const lines = [
    new TicketLine('1', null, '1,37', 'MELON PARTIDO', 'Melon partido', null, []),
    new TicketLine('1', null, '2,15', 'COCKTAIL TOST', 'Cocktail tostado', null, []),
    new TicketLine('2', null, '0,90', 'STAR II PLUS', 'Estrella de la muerte 2.0', null, []),
  ]
  const proprietaryCodes = [{ OP: '068391' }, { 'FACTURA SIMPLIFICADA': '2707-022-142004' }];
  const dummyTicket = new Ticket(
    store,
    new Date('2019-08-20T10:38'),
    proprietaryCodes,
    'CARD',
    '4,42',
    null,
    lines
  );
  const [ticket, setTicket] = useState(dummyTicket);
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
      if (elems) {
        setElements(elems);
      }
    };

    fetchData();
    console.log(`${new Date().toISOString()} - TicketViewContainer:useEffect:ticket`);
    console.log(ticket);
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
      <View style={styles.header}>
        <View style={styles.companyName}>
          <Text style={iOSUIKit.largeTitleEmphasized}>{ticket.store.company}</Text>
        </View>
        <View style={styles.companyInfo}>
          <View style={styles.companyInfoRow1}>
            <CardComponent
              title={`${ticket.store.city}, ${ticket.store.address}`}
              icon={<Icon reverse raised iconStyle={{ fontSize: 18 }} type="entypo" name="shop" color={iOSColors.orange} size={13} />}
            />
          </View>
          <View style={styles.companyInfoRow2}>
            <CardComponent
              title={ticket.store.phone}
              icon={<Icon reverse raised iconStyle={{ fontSize: 18 }} type="entypo" name="phone" color={iOSColors.green} size={13} />}
            />
            <CardComponent
              title={ticket.store.id}
              icon={<Icon reverse raised iconStyle={{ fontSize: 18 }} type="entypo" name="info" color={iOSColors.blue} size={13} />}
            />
          </View>
          <CardComponent
            title={ticket.datetime.toISOString()}
            icon={<Icon reverse raised iconStyle={{ fontSize: 18 }} type="entypo" name="calendar" color={iOSColors.red} size={13} />}
          />
        </View>
      </View>

      <FlatList
        style={styles.list}
        data={ticket.lines}
        renderItem={({ item, index }) => {
          console.log(item)
          return (
            <ListItem
              title={
                item.quantity +
                item.weight +
                item.price +
                item.name +
                item.readableName +
                item.id +
                item.altCodes
              }
              containerStyle={{ padding: 5 }}
              onPress={() => handlePressedLine(index)}
            />
          );
        }}
        keyExtractor={(item, index) => index.toString()}
      />
      <View style={styles.footer}>
        <CardComponent
          title={`Payment Method: ${ticket.paymentMethod}`}
          icon={<Icon reverse raised iconStyle={{ fontSize: 18 }} type="material-community" name="cash-register" color={iOSColors.lightGray2} size={13} />}
        />
        <CardComponent
          title={`Total: ${ticket.total}`}
          icon={<Icon reverse raised iconStyle={{ fontSize: 26 }} type="foundation" name="euro" color='mediumseagreen' size={13} />}
        />
        {/* <View style={styles.paymentMethod}><Text>PAYMENT METHOD: {ticket.paymentMethod}</Text></View> */}
        {/* <View style={styles.total}><Text>TOTAL: {ticket.total}</Text></View> */}
      </View>
      {/* <Button title="Save" style={styles.button} onPress={handleConfirmPress} /> */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    ...styleDebug('red'),
    flex: 1,
  },
  header: {
    // ...styleDebug('blue'),
    marginVertical: 5,
  },
  list: {
    ...styleDebug('darkgreen'),
  },
  footer: {
    // ...styleDebug('purple'),
    marginVertical: 5,
    marginHorizontal: 10,
  },
  companyName: {
    // ...styleDebug('orange'),
    alignSelf: 'center',
  },
  companyInfo: {
    // ...styleDebug('red'),
    marginHorizontal: 10,
  },
  companyInfoRow1: {
    // ...styleDebug('blue'),
    flexDirection: 'row',
  },
  companyInfoRow2: {
    // ...styleDebug('blue'),
    flexDirection: 'row',
    justifyContent: 'space-between',
  }
});

TicketViewContainer.propTypes = {};
TicketViewContainer.defaultProps = {};
