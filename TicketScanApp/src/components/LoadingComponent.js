import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Modal, Text, ActivityIndicator } from 'react-native';
import { iOSUIKit } from 'react-native-typography';

export default function LoadingComponent(props) {
  return (
    <View>
      <Modal visible={props.isLoading} transparent animationType="fade">
        <View style={styles.modalBackground}>
          <View style={styles.container}>
            {props.activityComponent}
            <Text style={styles.textLoading}>{props.loadingText}</Text>
          </View>
        </View>
      </Modal>
    </View>
  );
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
    // height: 100,
    maxWidth: 200,
    borderRadius: 10,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  textLoading: {
    ...iOSUIKit.subhead,
    marginTop: 10,
    flexWrap: 'wrap',
  }
});

LoadingComponent.propTypes = {
  loadingText: PropTypes.string,
  isLoading: PropTypes.bool.isRequired,
  activityComponent: PropTypes.element,
};
LoadingComponent.defaultProps = {
  loadingText: 'Loading...',
  activityComponent: <ActivityIndicator />,
};
