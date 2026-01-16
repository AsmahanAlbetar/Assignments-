library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity doorController is
  port (
    Clk   :        in std_logic;
    reset :        in std_logic; --Active low asynchronus reset
    sensor_in :    in std_logic; --  1 = open , 0 = close

    door_state_led :  out std_logic_vector(1 downto 0); 
    remaining_time :  out std_logic_vector(1 downto 0)
  ) ;
end doorController;

architecture arch of doorController is
type state is (opened, opening,closed, closing );

signal my_state : state:= closed;
signal counter  : integer := 0; 
signal opening_counter : integer:= 0;

begin 

process(clk, reset,sensor_in)

variable var_remaining_time: integer := 0;

begin

    if reset = '0' then
      my_state <= closed;
      counter  <= 0;
      opening_counter <= 0;
    --   var_remaining_time <= 0;
      door_state_led <= "00";
      remaining_time <= "00";

    elsif rising_edge(clk) then 

        case my_state is 

            when opened =>
                door_state_led <="10";
                remaining_time <= "10";
                counter <= 0 ;
                if counter < 10 then 
                    counter <= counter + 1;
                    -- var_remaining_time <= (10 - counter);
                else 
                    counter <= 0;
                    my_state<= closing;
                end if;
            when closing =>
                door_state_led <="11";
                counter <= 0;
                if counter < 5 then 
                    counter <= counter + 1;
                    if (sensor_in = '1') then 
                        door_state_led <= "01" ;--opening
                        if opening_counter < counter then 
                            opening_counter <= opening_counter +1;
                        else
                            opening_counter <= 0;
                            my_state <= opened;
                        end if;

                    end if; 
                else 
                    counter <= 0;
                    my_state<= closed;
                end if;
            when closed => 
                door_state_led <="00"; --closed
                if (sensor_in = '1') then 
                    my_state <= opening;
                end if;
            when opening =>
                    door_state_led <="01"; --closed
                    counter <= 0 ;
                    if counter < 5 then 
                        counter <= counter + 1;
                    else 
                        counter <= 0;
                        my_state<= opened;
                    end if;

        end case;
    end if;
end process;

    -- remaining_time <= var_remaning_time;


end architecture ; -- arch