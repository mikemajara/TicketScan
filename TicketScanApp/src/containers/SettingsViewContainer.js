import React from 'react';
import {
  View, //
  Alert,
} from 'react-native';
import { connect } from 'react-redux';
import SettingsList from 'react-native-settings-list';
import PropTypes from 'prop-types';
import { iOSColors, iOSUIKit } from 'react-native-typography';
import { changeSetting, deleteAllOps, deleteAllFavorites } from '../actions';

const BACKGROUND_COLOR = '#EFEFF4';
const ROW_SEPARATOR_COLOR = '#c8c7cc';
const ROW_MARGIN_TOP = 20;

const propTypes = {
  settings: PropTypes.shape({
    isAdditionEnabled: PropTypes.bool.isRequired,
    isSubtractionEnabled: PropTypes.bool.isRequired,
    isMultiplicationEnabled: PropTypes.bool.isRequired,
    isDivisionEnabled: PropTypes.bool.isRequired,
    isSynesthesiaEnabled: PropTypes.bool.isRequired,
    operationsPerRound: PropTypes.number.isRequired,
    level: PropTypes.number.isRequired,
  }).isRequired,
  handleSetting: PropTypes.func.isRequired,
  deleteAllOps: PropTypes.func.isRequired,
};

const defaultProps = {};

class SettingsViewContainer extends React.Component {
  static navigationOptions = {
    title: 'Settings', // Enable app header and use 'Settings' as the label
  };

  render() {
    const { settings, handleSetting, deleteAllOps, deleteAllFavorites } = this.props;
    const shouldBeDisabled = settingName => {
      return (
        settings[settingName] &&
        [
          settings.isAdditionEnabled,
          settings.isSubtractionEnabled,
          settings.isMultiplicationEnabled,
          settings.isDivisionEnabled,
        ].filter(x => x).length === 1
      )
    }
    return (
      <View style={{ backgroundColor: BACKGROUND_COLOR, flex: 1 }}>
        <View style={{ backgroundColor: BACKGROUND_COLOR, flex: 1 }}>
          <SettingsList borderColor={ROW_SEPARATOR_COLOR} defaultItemSize={46} borderWidth={0.5}>
            <SettingsList.Header headerStyle={{ marginTop: ROW_MARGIN_TOP }} />
            <SettingsList.Item
              hasSwitch
              switchState={settings.isAdditionEnabled}
              switchProps={{ disabled: shouldBeDisabled('isAdditionEnabled') }}
              switchOnValueChange={value => handleSetting({ id: 'isAdditionEnabled', value })}
              hasNavArrow={false}
              title="Addition"
            />
            <SettingsList.Item
              hasSwitch
              switchState={settings.isSubtractionEnabled}
              switchProps={{ disabled: shouldBeDisabled('isSubtractionEnabled') }}
              switchOnValueChange={value => handleSetting({ id: 'isSubtractionEnabled', value })}
              hasNavArrow={false}
              title="Subtraction"
            />
            <SettingsList.Item
              hasSwitch
              switchState={settings.isMultiplicationEnabled}
              switchProps={{ disabled: shouldBeDisabled('isMultiplicationEnabled') }}
              switchOnValueChange={value => handleSetting({ id: 'isMultiplicationEnabled', value })}
              hasNavArrow={false}
              title="Multiplication"
            />
            <SettingsList.Item
              hasSwitch
              switchState={settings.isDivisionEnabled}
              switchProps={{ disabled: shouldBeDisabled('isDivisionEnabled') }}
              switchOnValueChange={value => handleSetting({ id: 'isDivisionEnabled', value })}
              hasNavArrow={false}
              title="Division"
            />

            <SettingsList.Header headerStyle={{ marginTop: ROW_MARGIN_TOP }} />
            <SettingsList.Item
              title="Synesthesia"
              hasSwitch
              switchState={settings.isSynesthesiaEnabled}
              switchOnValueChange={value => handleSetting({ id: 'isSynesthesiaEnabled', value })}
              hasNavArrow={false}
            />

            <SettingsList.Header headerStyle={{ marginTop: ROW_MARGIN_TOP }} />
            <SettingsList.Item
              // icon={<Image style={styles.imageStyle} />}
              title="Number of operations per round"
              hasNavArrow={false}
              titleInfo={` ${settings.operationsPerRound}`}
              titleInfoStyle={{ fontSize: 20 }}
              onPress={() => {
                Alert.prompt(
                  'Operations per round',
                  'How many operations per training would you like to do?',
                  itemValue => {
                    handleSetting({ id: 'operationsPerRound', value: parseInt(itemValue, 10) });
                  },
                  'plain-text',
                  '',
                  'numeric'
                );
              }}
            />
            <SettingsList.Item
              // icon={<Image style={styles.imageStyle} />}
              title="Digits per operation"
              hasNavArrow={false}
              titleInfo={` ${settings.level}`}
              titleInfoStyle={{ fontSize: 20 }}
              onPress={() => {
                Alert.prompt(
                  'Number of digits per operation',
                  'How many digits do you want the operands to have in your training?',
                  itemValue => {
                    handleSetting({ id: 'level', value: parseInt(itemValue, 10) });
                  },
                  'plain-text',
                  '',
                  'numeric'
                );
              }}
            />
            {/* AlertIOS Not working, fixed wie so */}
            {/* The current signature is Alert.prompt(title, message, callbackOrButtons, 
            type, defaultValue, keyboardType) and the old syntax will be removed in a 
            future version.', */}
            {/* TODO Picker not working on device */}
            {/* <SettingsList.Header headerStyle={{ marginTop: ROW_MARGIN_TOP, marginLeft: 20 }} headerText={"Number of digits in operation"} />
            <PickerIOS
              selectedValue={settings.level}
              onValueChange={(itemValue) => this.handlePicker('level', itemValue)}>
              <PickerIOS.Item key="1" value="1" label="Digits 1" />
              <PickerIOS.Item key="2" value="2" label="Digits 2" />
              <PickerIOS.Item key="3" value="3" label="Digits 3" />
              <PickerIOS.Item key="4" value="4" label="Digits 4" />
              <PickerIOS.Item key="5" value="5" label="Digits 5" />
              <PickerIOS.Item key="6" value="6" label="Digits 6" />
              <PickerIOS.Item key="7" value="7" label="Digits 7" />
            </PickerIOS> */}
            <SettingsList.Header headerStyle={{ marginTop: ROW_MARGIN_TOP }} />
            <SettingsList.Item
              title="Delete operation history"
              titleStyle={[iOSUIKit.body, { textAlign: 'center', color: iOSColors.red }]}
              onPress={() =>
                Alert.alert(
                  'Delete all operations',
                  'This will permanently delete all the operations history',
                  [
                    {
                      text: 'Cancel',
                      style: 'cancel',
                    },
                    {
                      text: 'Delete',
                      style: 'destructive',
                      onPress: () => deleteAllOps(),
                    },
                  ]
                )}
              hasNavArrow={false}
            />
            <SettingsList.Item
              title="Unmark all favorites"
              titleStyle={[iOSUIKit.body, { textAlign: 'center', color: iOSColors.red }]}
              onPress={() =>
                Alert.alert(
                  'Delete favorites',
                  'This will permanently remove favorite tag from all operations. It will not remove operations themselves.',
                  [
                    {
                      text: 'Cancel',
                      style: 'cancel',
                    },
                    {
                      text: 'Delete',
                      style: 'destructive',
                      onPress: () => deleteAllFavorites(),
                    },
                  ]
                )
              }
              hasNavArrow={false}
            />
          </SettingsList>
        </View>
      </View>
    );
  }
}

const mapStateToProps = state => ({
  settings: state.settings,
});

const mapDispatchToProps = dispatch => ({
  handleSetting: setting => dispatch(changeSetting(setting)),
  deleteAllOps: () => dispatch(deleteAllOps()),
  deleteAllFavorites: () => dispatch(deleteAllFavorites()),
  dispatch,
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(SettingsViewContainer);

SettingsViewContainer.propTypes = propTypes;
SettingsViewContainer.defaultProps = defaultProps;
