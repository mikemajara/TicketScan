import React from 'react';
import { useState, useEffect } from 'react';
import Modal from 'react-native-modal';
import { View, Text, TouchableHighlight, Alert, StyleSheet } from 'react-native';
import { iOSColors, iOSUIKit, systemWeights } from 'react-native-typography';

import { styleDebug } from '../helpers';

export default function TicketLineDetailModal(props) {
  return (
    <Modal
      style={styles.modal}
      backdropColor="#00000040"
      onSwipeComplete={props.onPressClose}
      swipeDirection={['down']}
      isVisible={props.visible}
    >
      <View style={styles.container}>
        <Text>Hello World!</Text>

        <TouchableHighlight
          onPress={props.onPressClose}>
          <Text>Hide Modal</Text>
        </TouchableHighlight>
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
    padding: 20,
    flex: 1,
    marginTop: 400,
    justifyContent: 'center',
    alignItems: 'center',
    borderTopRightRadius: 20,
    borderTopLeftRadius: 20,
  },
});
