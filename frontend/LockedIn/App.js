import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createDrawerNavigator } from '@react-navigation/drawer';

// Import your other screens
import MainScreen from './components/MainScreen';
import AddChallengeScreen from './components/AddChallenge';

// Import the onboarding screens
import Onboarding from './components/Onboarding/OnboardingScreen';
import LoginScreen from './components/Onboarding/LoginScreen';
import SignUpScreen from './components/Onboarding/SignUp';

const Stack = createNativeStackNavigator();
const Drawer = createDrawerNavigator();

function DrawerNavigator() {
  return (
    <Drawer.Navigator initialRouteName="Main">
      <Drawer.Screen name="Main" component={MainScreen} />
      <Drawer.Screen name="AddChallenge" component={AddChallengeScreen} />
      {/* Add additional screens here */}
    </Drawer.Navigator>
  );
}

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Onboarding"
          component={Onboarding}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Signup"
          component={SignUpScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="DrawerNavigator"
          component={DrawerNavigator}
          options={{ headerShown: false }}
        />
        {/* Add additional screens here */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;
