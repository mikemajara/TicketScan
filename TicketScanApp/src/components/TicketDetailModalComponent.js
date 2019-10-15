import React from 'react';
import { useState, useEffect } from 'react';
import Modal from 'react-native-modal';
import { View, Text, TouchableHighlight, Alert, StyleSheet, TextInput } from 'react-native';
import { Icon } from 'react-native-elements';
import { iOSColors, iOSUIKit, systemWeights } from 'react-native-typography';
import { PropTypes } from 'prop-types';

import { styleDebug } from '../helpers';

export default function TicketLineDetailModal(props) {
  const { line } = props;
  const [name, setName] = useState(line.name);
  const [units, setUnits] = useState(line.units.toString());
  const [price, setPrice] = useState(line.price.toString());

  const saveLine = () => {
    props.lineUpdate({
      name,
      units: parseInt(units, 10),
      price: parseFloat(price),
    });
  };

  useEffect(() => {
    saveLine();
  }, [units, price, name]);

  const closeModal = e => {
    props.onPressClose(e);
  };

  const saveAndCloseModal = e => {
    saveLine(e);
    closeModal(e);
  };

  const sumUnits = value => {
    const oldValue = parseInt(units, 10);
    const sumValue = parseInt(value, 10);
    const result = oldValue + sumValue;
    if (result < 1) {
      setUnits('1');
    } else {
      setUnits(result.toString());
    }
  };

  const sumPrice = value => {
    const oldValue = parseFloat(price, 10);
    const sumValue = parseFloat(value, 10);
    const result = (oldValue + sumValue).toFixed(2);
    if (result < 0.01) {
      setPrice('0.01');
    } else {
      setPrice(result.toString());
    }
  };

  return (
    <Modal
      style={styles.modal}
      backdropOpacity={0.4}
      onSwipeComplete={props.onPressClose}
      swipeDirection={['down']}
      isVisible={props.visible}
      avoidKeyboard>
      <View style={styles.container}>
        <View style={{ position: 'absolute', top: -25, right: '47%' }}>
          <Icon type="feather" name="minus" color={iOSColors.lightGray2} size={63} />
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
            onPress={() => sumUnits(units < 1 ? 0 : -1)}
          />
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <TextInput
              style={[styles.textInputUnits, { borderWidth: StyleSheet.hairlineWidth, padding: 5, borderRadius: 7 }]}
              onChangeText={text => setUnits(text)}
              value={units}
              keyboardType="number-pad"
              onBlur={() => {
                if (Number.isNaN(units) || units < 1) {
                  setUnits('1');
                }
              }}
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
            onPress={() => sumUnits(1)}
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
            onPress={() => sumPrice(price <= 0.01 ? 0.01 : -0.01)}
          />
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <TextInput
              style={[styles.textInputPrice, { borderWidth: StyleSheet.hairlineWidth, padding: 5, borderRadius: 7 }]}
              onChangeText={text => setPrice(text)}
              value={price}
              onBlur={() => {
                if (Number.isNaN(price) || price < 0.01) {
                  setPrice('0.01');
                }
              }}
              keyboardType="numeric"
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
            onPress={() => sumPrice(0.01)}
          />
        </View>
      </View>
    </Modal >
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
    paddingHorizontal: 20,
    paddingVertical: 60,
    borderTopRightRadius: 20,
    borderTopLeftRadius: 20,
  },
  iconsHeaderContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
  },
  icon: {
    color: 'white',
    fontSize: 24,
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

TicketLineDetailModal.propTypes = {
  // isVisible: PropTypes.bool,
  line: PropTypes.object,
  lineUpdate: PropTypes.func.isRequired,
  onPressClose: PropTypes.func.isRequired,
};
TicketLineDetailModal.defaultProps = {
  // isVisible: false,
  line: {
    units: '0',
    name: '',
    price: '0.00',
  },
};
