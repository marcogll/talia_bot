# app/modules/servicios.py
"""
This module is responsible for providing information about the services offered.

It's a simple informational module that gives clients an overview of the
available services and can be expanded to provide more detailed information
or initiate a quoting process.
"""

def get_service_info():
    """
    Provides a brief overview of the available services.

    Currently, this function returns a hardcoded list of services. For a more
    dynamic and easily maintainable system, this information could be fetched
    from a database, a configuration file, or an external API.
    """
    # TODO: Fetch service details from a database or a configuration file to
    # make the service list easier to manage and update.
    return "Ofrecemos una variedad de servicios, incluyendo:\n\n- Consultoría Estratégica\n- Desarrollo de Software\n- Talleres de Capacitación\n\n¿Sobre cuál te gustaría saber más?"
