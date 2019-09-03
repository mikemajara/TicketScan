import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View } from 'react-native';
import Ionicons from 'react-native-vector-icons/Ionicons'

export default function CardComponent(props) {
  return (
    <View styles={[styles.container, props.containerStyle]}>
      {props.title}
      {props.icon}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {

  }
});

CardComponent.propTypes = {};
CardComponent.defaultProps = {};