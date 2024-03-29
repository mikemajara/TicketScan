import React from 'react';
import { useState, useEffect } from 'react';

import PropTypes from 'prop-types';
import { StyleSheet, View, Alert, Text, FlatList, Modal, TouchableHighlight } from 'react-native';
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
import LoadingComponent from '../components/LoadingComponent';
import TicketLineDetailModal from '../components/TicketDetailModalComponent';

moment.locale('es');

export default function TicketViewContainer(props) {
  const ticketRepository = new TicketRepository();

  const emptyLoading = { isLoading: false, message: '' };
  const [ticket, setTicket] = useState(props.navigation.getParam('ticket', null));
  const [loading, setLoading] = useState(emptyLoading);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(null);

  const handleModifiedLine = async modifiedLine => {
    ticket.lines[selectedIndex] = { ...ticket.lines[selectedIndex], ...modifiedLine };
    setTicket({
      ...ticket,
      lines: [...ticket.lines],
    });
    await ticketRepository.update(ticket);
  };

  const handlePressedLine = index => {
    setSelectedIndex(index);
    setIsModalVisible(true);
  };

  if (ticket === null) {
    return (
      <View>
        <LoadingComponent isLoading={loading.isLoading} loadingText={loading.message} />
      </View>
    );
  }
  return (
    <View style={styles.container}>
      {selectedIndex != null && (
        <TicketLineDetailModal
          line={ticket.lines[selectedIndex]}
          visible={isModalVisible}
          onPressClose={() => {
            setIsModalVisible(false);
            setSelectedIndex(null);
          }}
          lineUpdate={modifiedLine => handleModifiedLine(modifiedLine)}
        />
      )}
      {loading.isLoading && (
        <LoadingComponent isLoading={loading.isLoading} loadingText={loading.message} />
      )}
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
          return (
            <AppleStyleSwipeableRow
              deleteContent={<Icon type="ionicon" name="ios-trash" color="white" size={35} />}
              flagContent={<Icon type="ionicon" name="ios-star" color="white" size={35} />}>
              <ProductListItemComponent
                units={item.units}
                name={item.name}
                price={item.price}
                total={item.total}
                weight={item.weight}
                weightPrice={item.weightPrice}
                subtitle=""
                bottomDivider={Boolean(ticket.lines.length - index - 1)}
                onPress={() => {
                  handlePressedLine(index);
                }}
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
        keyExtractor={(item, index) => index.toString()}
      />
      <View style={styles.footer}>
        <CardComponent
          title={`${ticket.payment_information.method}`}
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
          title={`${ticket.payment_information.total}`}
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
      </View>
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
