import React from 'react';
import { View, Text, Button } from 'react-native';

const AddChallengeScreen = () => {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Add your own challenge!</Text>
      <Button title="Click It" />
    </View>
  );
};

export default AddChallengeScreen;
