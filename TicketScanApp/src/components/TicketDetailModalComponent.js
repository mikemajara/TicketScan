import React from 'react';
import { useState, useEffect } from 'react';
import { View, Text, TouchableHighlight, Modal, Alert, StyleSheet } from 'react-native';
import { iOSColors, iOSUIKit, systemWeights } from 'react-native-typography';

import { styleDebug } from '../helpers';

export default function TicketLineDetailModal(props) {
  return (
    <Modal
      style={styles.modal}
      animationType="fade"
      transparent
      visible={props.visible}
      onRequestClose={() => {
        Alert.alert('Modal has been closed.');
      }}>
      <View style={styles.modalBackground}>
        <View style={styles.container}>
          <Text>Hello World!</Text>

          <TouchableHighlight
            onPress={props.onPressClose}>
            <Text>Hide Modal</Text>
          </TouchableHighlight>
        </View>
      </View>
    </Modal>
  )
}

const styles = StyleSheet.create({
  modalBackground: {
    flex: 1,
    alignItems: 'center',
    flexDirection: 'column',
    justifyContent: 'space-around',
    backgroundColor: '#00000040',
  },
  container: {
    backgroundColor: '#FFFFFF',
    padding: 10,
    height: 100,
    width: 200,
    borderRadius: 10,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  }
});
