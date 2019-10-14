import React from 'react';
import { useState, useEffect } from 'react';
import Modal from 'react-native-modal';
import { View, Text, TouchableHighlight, Alert, StyleSheet, TextInput } from 'react-native';
import { Icon } from 'react-native-elements';
import { iOSColors, iOSUIKit, systemWeights } from 'react-native-typography';

import { styleDebug } from '../helpers';

export default function TicketLineDetailModal(props) {
  // const { ticketLine } = props.ticketLine;
  const [name, setName] = useState('PAN BIMBO');
  const [units, setUnits] = useState(1);
  const [price, setPrice] = useState(1.0);

  const updateUnits = newValue => {
    if (Number.isNaN(newValue) || newValue < 0) {
      setUnits(0);
    } else {
      setUnits(newValue);
    }
  }

  const updatePrice = newValue => {
    if (Number.isNaN(newValue) || newValue < 0) {
      setPrice(0);
    } else {
      setPrice(newValue);
    }
  }

  return (
    <Modal
      style={styles.modal}
      backdropOpacity={0.4}
      onSwipeComplete={props.onPressClose}
      swipeDirection={['down']}
      isVisible={props.visible}
      avoidKeyboard
      coverScreen
    >
      <View style={styles.container}>
        <View style={styles.iconCloseContainer}>
          <Icon
            reverse
            type='ionicon'
            name='md-close'
            color={iOSColors.customGray}
            iconStyle={[styles.icon, { color: 'black' }]}
            size={13}
            onPress={props.onPressClose}
          />
        </View>
        <View style={{ flexDirection: 'row', justifyContent: 'center', alignSelf: 'center', borderWidth: StyleSheet.hairlineWidth, padding: 5, borderRadius: 7 }}>
          <TextInput
            style={styles.textInputName}
            onChangeText={text => setName(text)}
            value={name}
          />
        </View>
        <View style={styles.textInputUnitsContainer}>
          <Icon
            reverse
            type='ionicon'
            name='ios-remove'
            color={iOSColors.red}
            iconStyle={styles.icon}
            size={13}
            onPress={() => updateUnits(units <= 1 ? 1 : units - 1)}
          />
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <TextInput
              style={[styles.textInputUnits, { borderWidth: StyleSheet.hairlineWidth, padding: 5, borderRadius: 7 }]}
              onChangeText={text => updateUnits(parseInt(text, 10))}
              value={units.toString()}
            />
            <Text style={styles.textLabel}>Unidades</Text>
          </View>
          <Icon
            reverse
            type='ionicon'
            name='ios-add'
            color={iOSColors.green}
            iconStyle={styles.icon}
            size={13}
            onPress={() => updateUnits(units + 1)}
          />
        </View>
        <View style={styles.textInputPriceContainer}>
          <Icon
            reverse
            type='ionicon'
            name='ios-remove'
            color={iOSColors.red}
            iconStyle={styles.icon}
            size={13}
            onPress={() => updatePrice(price <= 0.01 ? 0.01 : price - 0.01)}
          />
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <TextInput
              style={[styles.textInputPrice, { borderWidth: StyleSheet.hairlineWidth, padding: 5, borderRadius: 7 }]}
              onChangeText={text => updatePrice(parseFloat(text, 10))}
              value={price.toString()}
            />
            <Text style={styles.textLabel}> € Unidad</Text>
          </View>
          <Icon
            reverse
            type='ionicon'
            name='ios-add'
            color={iOSColors.green}
            iconStyle={styles.icon}
            size={13}
            onPress={() => updatePrice(price + 0.01)}
          />
        </View>
      </View>
    </Modal>
  )
}

const styles = StyleSheet.create({
  modal: {
    justifyContent: 'flex-end',
    marginBottom: 0,
    marginHorizontal: 0,
  },
  container: {
    ...styleDebug('red'),
    backgroundColor: 'white',
    height: 300,
    justifyContent: 'space-between',
    padding: 20,
    paddingBottom: 50,
    borderTopRightRadius: 20,
    borderTopLeftRadius: 20,
  },
  iconCloseContainer: {
    alignSelf: 'flex-end',
  },
  icon: {
    color: 'white',
    fontSize: 18,
  },
  textLabel: {
    ...iOSUIKit.title3,
    ...systemWeights.light,
    marginLeft: 5,
  },
  textInputNameContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
  },
  textInputName: {
    ...iOSUIKit.body,
    ...systemWeights.light,
  },
  textInputUnitsContainer: {
    ...styleDebug('purple'),
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  textInputUnits: {
    ...styleDebug('green'),
    ...iOSUIKit.title3,
    ...systemWeights.light,
  },
  textInputPriceContainer: {
    ...styleDebug('purple'),
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  textInputPrice: {
    ...styleDebug('green'),
    ...iOSUIKit.title3,
    ...systemWeights.light,
  },
});
