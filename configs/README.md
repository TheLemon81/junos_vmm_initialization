This folder is where you will add non-set config statements.  The files here are referenced in the main py script.

groups { 

    routing-default { 

        interfaces { 

            <ge-*> { 

                mtu 9000; 

                unit <*> { 

                    family iso; 

                    family mpls {        

                        maximum-labels 16; 

                    } 

                } 

            } 

        } 

        protocols { 

            isis { 

                interface <*> { 

                    level 1 disable; 

                } 

            } 

        } 

    } 

} 

apply-groups routing-default; 
