import React from 'react';
import { useState, useEffect } from 'react';
import Modal from 'react-native-modal';
import { View, Text, TouchableHighlight, Alert, StyleSheet, TextInput } from 'react-native';
import { Icon } from 'react-native-elements';
import { iOSColors, iOSUIKit, systemWeights } from 'react-native-typography';

import { styleDebug } from '../helpers';

export default function TicketLineDetailModal(props) {
  // const { ticketLine } = props.ticketLine;
  const [units, setUnits] = useState(1);
  const [name, setName] = useState('PAN BIMBO');

  return (
    <Modal
      style={styles.modal}
      backdropColor="#00000040"
      onSwipeComplete={props.onPressClose}
      swipeDirection={['down']}
      isVisible={props.visible}
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
        <View style={styles.textInputUnitsContainer}>
          <Text style={styles.textLabel}>Unidades</Text>
          <Icon
            reverse
            type='ionicon'
            name='ios-remove'
            color={iOSColors.red}
            iconStyle={styles.icon}
            size={7}
            onPress={() => setUnits(units + 1)}
          />
          <TextInput
            style={styles.textInputUnits}
            onChangeText={text => setUnits(parseInt(text, 10))}
            value={units.toString()}
          />
          <Icon
            reverse
            type='ionicon'
            name='ios-add'
            color={iOSColors.green}
            iconStyle={styles.icon}
            size={7}
            onPress={() => setUnits(units <= 1 ? 1 : units - 1)}
          />
        </View>
        <View style={styles.textInputNameContainer}>
          <Text style={styles.textLabel}>Nombre</Text>
          <TextInput
            style={styles.textInputName}
            onChangeText={text => setName(text)}
            value={name}
          />
        </View>
      </View>
    </Modal>
  )
}

const styles = StyleSheet.create({
  modal: {
    marginHorizontal: 0,
    marginBottom: 0,
  },
  container: {
    ...styleDebug('red'),
    backgroundColor: 'white',
    flex: 1,
    justifyContent: 'space-between',
    padding: 20,
    paddingBottom: 100,
    marginTop: 400,
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
    marginRight: 10,
  },
  textInputUnitsContainer: {
    ...styleDebug('purple'),
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'baseline',
  },
  textInputUnits: {
    ...styleDebug('green'),
    ...iOSUIKit.title3,
    ...systemWeights.light,
  },
  textInputNameContainer: {
    alignItems: 'baseline',
    flexDirection: 'row',
  },
  textInputName: {
    ...iOSUIKit.body,
    ...systemWeights.light,
  },
});
