import React from 'react';
import { useState, useEffect } from 'react';

import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList } from 'react-native';
import { Button, ListItem, Icon } from 'react-native-elements';
// import { Animated } from 'react-native-reanimated';
import { iOSUIKit, iOSColors } from 'react-native-typography';
import Entypo from 'react-native-vector-icons/Entypo';
import moment from 'moment/min/moment-with-locales';
import { styleDebug, mockupTicket } from '../helpers';
import Ticket from '../model/Ticket';
import Store from '../model/Store';
import TicketLine from '../model/TicketLine';
import Company from '../model/Company';
import CardComponent from '../components/CardComponent';
import AppleStyleSwipeableRow from './AppleStyleSwipeableRow';
import ProductListItemComponent from '../components/ProductListItemComponent';
import TicketRepository from '../repository/TicketRepository';

moment.locale('es');

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

const ticketRepository = new TicketRepository();

export default function TicketViewContainer(props) {

  let company;// = Object.assign(new Company, ticket.company)
  let store;// = Object.assign(new Store, ticket.store)

  company = new Company(
    'id: string',
    'Mercadona S.A.',
    'A-1324122',
    '',
  );
  store = new Store(
    'Mercadona',
    'Spain',
    'Murcia',
    'AVDA. CICLISTA MARIANO ROJAS-AV',
    '+34 968227166',
    'A-46103834'
  );
  const lines = [
    new TicketLine('1', 'B, ALMENDRA S/A', '8,40', null, null, 'readableName', null, []),
    new TicketLine('4', 'L SEMI S/LACTO', '18,00', null, null, 'readableName', null, []),
    new TicketLine('3', 'GALLETA RELIEV', '3,66', null, null, 'readableName', null, []),
    new TicketLine('1', 'COPOS AVENA', '0,81', null, null, 'readableName', null, []),
    new TicketLine('1', 'COSTILLA BARB', '3,99', null, null, 'readableName', null, []),
    new TicketLine('1', 'ZANAHORIA BOLS', '0,69', null, null, 'readableName', null, []),
    new TicketLine('2', 'VENTRESCA ATUN', '4,30', null, null, 'readableName', null, []),
    new TicketLine('1', 'PAPEL HIGIENIC', '2,70', null, null, 'readableName', null, []),
    new TicketLine('1', 'HIGIENICO DOBL', '2,07', null, null, 'readableName', null, []),
    new TicketLine('1', 'PEPINO', '0,90', '0,478 kg', '1,89 €/kg', 'readableName', null, []),
    new TicketLine('1', 'PLATANO', '1,41', '0,616 kg', '2,29 €/kg', 'readableName', null, []),
  ];
  // const proprietaryCodes = [{ OP: '068391' }, { 'FACTURA SIMPLIFICADA': '2707-022-142004' }];
  const dummyTicket = new Ticket(
    company,
    store,
    new Date('2019-03-04T19:51'),
    null,
    'CARD',
    '46,93',
    null,
    lines
  );

  // Store constructor(company, country, city, address, phone, id) {
  // TicketLine constructor(units, name, price, weight, weightPrice, readableName, id, altCodes) {
  // Ticket constructor(store, datetime, proprietaryCodes, paymentMethod, total, returned, ticketLines) {

  const [ticketId, setTicketId] = useState(props.navigation.getParam('_id', null));
  const [elements, setElements] = useState([]);
  const [ticket, setTicket] = useState(null);

  useEffect(() => {
    // const fetchData = async () => {
    //   console.log('fetching data...');
    //   let elems = {};
    //   if (ticketId) {
    //     elems = await retrieveTicket(ticketId);
    //   } else {
    //     elems = props.navigation.getParam('elements', {});
    //   }
    //   elems = Object.values(elems);
    //   if (elems) {
    //     setElements(elems);
    //   }
    // };

    const fetchData = async () => {
      const t = await ticketRepository.findOne('5d9ccfaa8473b4c0f4622d9e');
      setTicket(t);
    };

    fetchData();

    console.log(`${new Date().toISOString()} - TicketViewContainer:113:ticket`);
    console.log(ticket);
  }, []);

  const handlePressedLine = index => {
    Alert.prompt(
      'Edit',
      'Correct the line as you see fit',
      async itemValue => {
        const arr = [...ticket.lines];
        arr[index] = JSON.parse(itemValue);
        const newTicket = { ...ticket, lines: arr };
        try {
          await ticketRepository.update(newTicket);
          setTicket(newTicket);
        } catch (error) {
          throw new Error('Exception handling not implemented');
        }
      },
      'plain-text',
      JSON.stringify(ticket.lines[index]),
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


  if (ticket === null) {
    return (
      <View>
        <Text>Loading...</Text>
      </View>
    )
  }
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.companyName}>
          <Text style={iOSUIKit.largeTitleEmphasized}>{ticket.company.name}</Text>
        </View>
        <View style={styles.companyInfo}>
          <View style={styles.companyInfoRow1}>
            <CardComponent
              title={`${ticket.store.city}, ${ticket.store.address}`}
              icon={
                <Icon
                  reverse
                  raised
                  iconStyle={{ fontSize: 18 }}
                  type="entypo"
                  name="shop"
                  color={iOSColors.orange}
                  size={13}
                />
              }
            />
          </View>
          <View style={styles.companyInfoRow2}>
            <CardComponent
              title={ticket.store.phone}
              icon={
                <Icon
                  reverse
                  raised
                  iconStyle={{ fontSize: 18 }}
                  type="entypo"
                  name="phone"
                  color={iOSColors.green}
                  size={13}
                />
              }
            />
            <CardComponent
              title={ticket.store.id}
              icon={
                <Icon
                  reverse
                  raised
                  iconStyle={{ fontSize: 18 }}
                  type="entypo"
                  name="info"
                  color={iOSColors.blue}
                  size={13}
                />
              }
            />
          </View>
          <CardComponent
            title={moment(ticket.datetime).format('llll')}
            icon={
              <Icon
                reverse
                raised
                iconStyle={{ fontSize: 18 }}
                type="entypo"
                name="calendar"
                color={iOSColors.red}
                size={13}
              />
            }
          />
        </View>
      </View>

      <FlatList
        style={styles.list}
        data={ticket.lines}
        renderItem={({ item, index }) => {
          console.log(item, ticket.lines.length, index);
          return (
            <AppleStyleSwipeableRow
              deleteContent={<Icon type="ionicon" name="ios-trash" color="white" size={35} />}
              // onPressDelete={() => {
              //   LayoutAnimation.configureNext(CustomLayoutLinear);
              //   this.props.deleteOp(item.id);
              // }}
              flagContent={<Icon type="ionicon" name="ios-star" color="white" size={35} />}
            // onPressFlag={() => {
            //   this.props.toggleFavorite(item.id);
            //   this.closeOpenRows();
            // }}
            // onSwipeableWillOpen={swipeable => this.closeOpenRows()}
            // onSwipeableOpen={swipeable => this.setOpenRow(swipeable)}
            // ref={ref => {
            //   this.swipeables[item.id] = ref;
            // }}
            >
              <ProductListItemComponent
                units={item.units}
                name={item.name}
                price={item.price}
                total={item.total}
                weight={item.weight}
                weightPrice={item.weightPrice}
                subtitle=""
                bottomDivider={Boolean(ticket.lines.length - index - 1)}
                onPress={() => handlePressedLine(index)}
                leftIcon={
                  <Icon
                    type="ionicon"
                    name="ios-star"
                    color={index % 2 ? iOSColors.yellow : 'transparent'}
                    size={15}
                  />
                }
              />
              {/* <ListItem
                title={
                  item.units +
                  item.weight +
                  item.price +
                  item.name +
                  item.readableName +
                  item.id +
                  item.altCodes
                }
                containerStyle={{ padding: 5 }}
                onPress={() => handlePressedLine(index)}
              /> */}
            </AppleStyleSwipeableRow>
          );
        }}
        keyExtractor={(item, index) => index.toString()}
      />
      <View style={styles.footer}>
        <CardComponent
          title={`${ticket.paymentInformation.method}`}
          icon={
            <Icon
              reverse
              raised
              iconStyle={{ fontSize: 18 }}
              type="material-community"
              name="cash-register"
              color={iOSColors.lightGray2}
              size={13}
            />
          }
        />
        <CardComponent
          title={`${ticket.paymentInformation.total}`}
          icon={
            <Icon
              reverse
              raised
              iconStyle={{ fontSize: 26 }}
              type="foundation"
              name="euro"
              color="mediumseagreen"
              size={13}
            />
          }
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
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: iOSColors.lightGray2,
    paddingVertical: 5,
  },
  list: {
    ...styleDebug('darkgreen'),
  },
  footer: {
    // ...styleDebug('purple'),
    flexDirection: 'row',
    justifyContent: 'space-between',
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: iOSColors.lightGray2,
    paddingVertical: 5,
    paddingHorizontal: 10,
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
  },
});

TicketViewContainer.propTypes = {};
TicketViewContainer.defaultProps = {};
