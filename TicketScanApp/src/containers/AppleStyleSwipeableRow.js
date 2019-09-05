import React, { Component } from 'react';
import { Animated, StyleSheet, Text, View } from 'react-native';

import { RectButton } from 'react-native-gesture-handler';

import Swipeable from 'react-native-gesture-handler/Swipeable';
import PropTypes from 'prop-types';
import { styleDebug } from '../helpers';

export default class AppleStyleSwipeableRow extends Component {
  renderLeftActions = (progress, dragX) => {
    const trans = dragX.interpolate({
      inputRange: [0, 50, 100, 101],
      outputRange: [-20, 0, 0, 1],
    });
    return (
      <RectButton style={styles.leftAction} onPress={this.close}>
        <Animated.Text
          style={[
            styles.actionText,
            {
              transform: [{ translateX: trans }],
            },
          ]}>
          Archive
        </Animated.Text>
      </RectButton>
    );
  };

  renderRightAction = (content, text, color, x, progress, onPress) => {
    const trans = progress.interpolate({
      inputRange: [0, 1],
      outputRange: [x, 0],
    });
    const pressHandler = () => {
      this.close();
      alert(text);
    };
    return (
      <Animated.View style={{ flex: 1, transform: [{ translateX: trans }] }}>
        <RectButton style={[styles.rightAction, { backgroundColor: color }]} onPress={onPress}>
          {content}
          {text ? <Text style={styles.actionText}>{text}</Text> : null}
        </RectButton>
      </Animated.View>
    );
  };

  renderRightActions = progress => {
    const {
      moreContent,
      flagContent,
      deleteContent,
      onPressMore,
      onPressFlag,
      onPressDelete,
    } = this.props;
    const cellWidth = 64;
    const width =
      cellWidth * (Boolean(moreContent) + Boolean(flagContent) + Boolean(deleteContent));
    const moreX = 64 * (Boolean(moreContent) + Boolean(flagContent) + Boolean(deleteContent));
    const flagX = 64 * (Boolean(flagContent) + Boolean(deleteContent));
    const deleteX = 64 * Boolean(deleteContent);
    return (
      <View style={{ width, flexDirection: 'row-reverse' }}>
        {deleteContent
          ? this.renderRightAction(deleteContent, '', '#dd2c00', deleteX, progress, onPressDelete)
          : null}
        {flagContent
          ? this.renderRightAction(flagContent, '', '#ffab00', flagX, progress, onPressFlag)
          : null}
        {moreContent
          ? this.renderRightAction(moreContent, '', '#C8C7CD', moreX, progress, onPressMore)
          : null}
      </View>
    );
  };

  updateRef = ref => {
    this._swipeableRow = ref;
  };

  close = () => {
    this._swipeableRow.close();
  };

  render() {
    const { children } = this.props;
    return (
      <Swipeable
        ref={this.updateRef}
        friction={2}
        leftThreshold={140}
        rightThreshold={50}
        // renderLeftActions={this.renderLeftActions}
        renderRightActions={this.renderRightActions}
        onSwipeableOpen={() => {
          this.props.onSwipeableOpen(this._swipeableRow);
        }}
        onSwipeableWillOpen={() => {
          this.props.onSwipeableWillOpen(this._swipeableRow);
        }}>
        {children}
      </Swipeable>
    );
  }
}

const styles = StyleSheet.create({
  leftAction: {
    flex: 1,
    backgroundColor: '#497AFC',
    justifyContent: 'center',
  },
  actionText: {
    color: 'white',
    fontSize: 16,
    backgroundColor: 'transparent',
    // padding: 10,
  },
  rightAction: {
    ...styleDebug('purple'),
    alignItems: 'center',
    flex: 1,
    justifyContent: 'center',
  },
});

AppleStyleSwipeableRow.propTypes = {
  onSwipeableOpen: PropTypes.func,
  onSwipeableWillOpen: PropTypes.func,
};
AppleStyleSwipeableRow.defaultProps = {
  onSwipeableOpen: () => { },
  onSwipeableWillOpen: () => { },
};
