import 'package:flutter/material.dart';

void main() {
  runApp(SmartHomeAssistant());
}

class SmartHomeAssistant extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: AlertSettingsPage(),
    );
  }
}

class AlertSettingsPage extends StatefulWidget {
  @override
  _AlertSettingsPageState createState() => _AlertSettingsPageState();
}

class _AlertSettingsPageState extends State<AlertSettingsPage> {
  List<String> alerts = [
    'The door of the fridge is open',
    'My cat is on the kitchen countertop',
    'The stove is not turned off'
  ];
  List<String> selectedAlerts = [];
  TextEditingController _newAlertController = TextEditingController();

  @override
  void dispose() {
    _newAlertController.dispose();
    super.dispose();
  }

  void _addNewAlert() {
    if (_newAlertController.text.isNotEmpty) {
      setState(() {
        alerts.add(_newAlertController.text);
        _newAlertController.clear();
      });
    }
  }

  void _saveSettings() {
    // Add logic to save settings
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Settings saved successfully!')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Smart Home Assistant'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Choose when you want to be alerted:',
              style: TextStyle(fontSize: 20),
            ),
            SizedBox(height: 10),
            TextField(
              controller: _newAlertController,
              decoration: InputDecoration(
                labelText: 'Add a new alert',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: _addNewAlert,
              child: Text('Add Alert'),
            ),
            SizedBox(height: 20),
            Expanded(
              child: ListView(
                children: alerts.map((alert) {
                  return CheckboxListTile(
                    title: Text(alert),
                    value: selectedAlerts.contains(alert),
                    onChanged: (bool? value) {
                      setState(() {
                        if (value == true) {
                          selectedAlerts.add(alert);
                        } else {
                          selectedAlerts.remove(alert);
                        }
                      });
                    },
                  );
                }).toList(),
              ),
            ),
            Center(
              child: ElevatedButton(
                onPressed: _saveSettings,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.purple[100], // Light purple color
                ),
                child: Text(
                  'Save Settings',
                  style: TextStyle(color: Colors.black), // White text color
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
