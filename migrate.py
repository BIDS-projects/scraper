from mapping import migration_manager, MigrateCommand

migration_manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    migration_manager.run()
